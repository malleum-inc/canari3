from __future__ import print_function

import math
import sys
import os
import shutil
import tempfile
import zipfile

from mimetypes import guess_type
from hashlib import md5

import boto3

from six import b
from six.moves import urllib
from mrbob.configurator import Configurator

import canari
from canari.commands.common import canari_main
from canari.commands.framework import SubCommand, Argument
from canari.pkgutils.transform import TransformDistribution
from canari.resource import image_resources
from canari.project import CanariProject
from canari.utils.fs import PushDir

if sys.version_info[0] > 2:
    from queue import Queue
else:
    from Queue import Queue


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

S3_CDN_BUCKET_POLICY = """{
    "Version":"2012-10-17",
    "Statement":[{
        "Sid":"PublicReadGetObject",
        "Effect":"Allow",
        "Principal": "*",
        "Action":["s3:GetObject"],
        "Resource":["arn:aws:s3:::%s/*"]
    }]
}"""

DEPENDENCY_FILE_NAME = 'canari3-%s-aws-lambda-deps-py%s.zip' % (canari.__version__, sys.version_info[0])

DEPENDENCY_DOWNLOAD_URL = os.environ.get(
    'DEPS_DOWNLOAD_URL',
    'https://github.com/redcanari/canari3/releases/download/v%s/%s' % (canari.__version__, DEPENDENCY_FILE_NAME)
)

# Queue for blocking until we get a result from hook to setup(). Ugly but effective :P
q = Queue()


def setup_hook(**kwargs):
    print("Gathering package requirements for %s..." % kwargs['name'], file=sys.stderr)
    q.put(([r for r in kwargs.get('install_requires', []) if not r.startswith('canari')]))


def hook_setup():
    import setuptools
    setuptools.setup = setup_hook


def get_dependencies(project):
    with PushDir(project.root_dir):
        hook_setup()
        import setup
    return set(q.get())


def download_progress(count, size, total_bytes):
    if not total_bytes or not size:
        print('Downloading %s...' % DEPENDENCY_FILE_NAME)

    total_count = math.ceil(float(total_bytes)/size)
    percent_done = count / total_count
    print('Downloading %s |%-20s| %.2f complete' % (
        DEPENDENCY_FILE_NAME,
        '#' * int(percent_done * 20),
        percent_done * 100
    ), end='\r' if count < total_count else '\n', file=sys.stderr)


def upload_images(project, opts):
    bucket = opts.bucket or md5(b('canari-%s-transform-images' % project.name)).hexdigest()
    region = opts.region_name or boto3.session.Session().region_name
    base_url = 'about:blank'

    with PushDir(project.src_dir):
        imgs = image_resources(project.name)

        if not imgs:
            return base_url

        print('Uploading image resources to AWS S3 bucket %r' % bucket, file=sys.stderr)
        s3 = boto3.client(
            's3',
            # Hard coded strings as credentials, not recommended.
            aws_access_key_id=opts.aws_access_key_id,
            aws_secret_access_key=opts.aws_secret_access_key,
            region_name=region
        )

        if bucket not in [bkt['Name'].lower() for bkt in s3.list_buckets()['Buckets']]:
            print('Creating S3 bucket %r because it does not exist' % bucket)
            s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': region})

        for i in imgs:
            img_name = os.path.basename(i)
            dst_path = 'static/%s' % md5(b(img_name)).hexdigest()
            print('Uploading %r to %r...' % (i, dst_path))
            s3.upload_file(i, bucket, dst_path, ExtraArgs={'ContentType': guess_type(i)[0]})

        print('Creating static website configuration for bucket %r...' % bucket)
        s3.put_bucket_website(Bucket=bucket, WebsiteConfiguration={'IndexDocument': {'Suffix': 'index.html'}})

        print('Adjusting bucket policy for public GetObject access...')
        s3.put_bucket_policy(Bucket=bucket, Policy=S3_CDN_BUCKET_POLICY % bucket)

        base_url = 'http://%s.s3-website.%s.amazonaws.com/static/' % (bucket, region)
        print('Static images are now hosted at %r!' % base_url)

    return base_url


@SubCommand(
    canari_main,
    help="Adds AWS Lambda capability.",
    description="Creates an AWS Chalice project for deployment to lambda."
)
@Argument(
    '-b',
    '--bucket',
    metavar='<S3 bucket name>',
    help="The name of the bucket to store image and other binary resources for transforms in."
)
@Argument(
    '-r',
    '--region-name',
    default=None,
    metavar='<AWS region>',
    help="The region to store the S3 objects in"
)
@Argument(
    '-k',
    '--aws-access-key-id',
    default=None,
    metavar='<AWS access key ID>',
    help="AWS access key ID"
)
@Argument(
    '-s',
    '--aws-secret-access-key',
    metavar='<AWS secret access key>',
    help="AWS secret access key"
)
def create_aws_lambda(opts):
    try:
        project = CanariProject()
        target = os.path.join(project.root_dir, 'aws')

        with PushDir(project.src_dir):
            transform_package = TransformDistribution(project.name)
            if not transform_package.remote_transforms:
                print("No remote transforms found in %r... exiting" % project.name)
                exit(-1)

            cdn_base_url = upload_images(project, opts)

            variables = {
                'project.name': project.name,
                'project.requirements': get_dependencies(project),
                'package.transforms': [t() for t in transform_package.remote_transforms],
                'image.cdn': cdn_base_url
            }

            configurator = Configurator(
                'canari.resources.templates:create_aws_lambda',
                target,
                {'non_interactive': True},
                variables=variables
            )

            print('Generating Chalice project for %r in %r...' % (project.name, target), file=sys.stderr)
            configurator.ask_questions()
            configurator.render()

            transform_package.configure(os.path.join(target, 'chalicelib'), remote=True, additional_options={
                'cdn': cdn_base_url
            })

            dst_dir = '../aws/vendor/%s' % project.name
            if os.path.lexists(dst_dir):
                shutil.rmtree(dst_dir)

            print("Copying %r project tree to the 'aws' directory..." % project.name, file=sys.stderr)
            shutil.copytree(project.name, dst_dir,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".*", "*.gif", "*.jpg", "*.jpeg",
                                                          "*.png", "*.whl"))

            deps_dst = os.path.join(tempfile.gettempdir(), DEPENDENCY_FILE_NAME)
            try:
                print("Copying Amazon dependencies for Canari to the 'aws/vendor' directory...", file=sys.stderr)
                if not os.path.lexists(deps_dst):
                    print("Downloading dependencies from %r... " % DEPENDENCY_DOWNLOAD_URL, file=sys.stderr)
                    deps_dst, _ = urllib.request.urlretrieve(
                        DEPENDENCY_DOWNLOAD_URL, deps_dst, reporthook=download_progress)
                else:
                    print("Using cached dependencies from %r" % deps_dst)

                print("Decompressing dependencies into 'aws/vendor'", file=sys.stderr)
                zip_file = zipfile.ZipFile(deps_dst, 'r')
                zip_file.extractall("../aws/vendor")
                zip_file.close()
            except IOError:
                if os.path.lexists(deps_dst):
                    os.unlink(deps_dst)
                print("Failed to download dependencies from %r..." % DEPENDENCY_DOWNLOAD_URL)
                exit(-1)

            print("To deploy type 'chalice deploy' in the %r directory" % target, file=sys.stderr)
            print('done!', file=sys.stderr)
    except ValueError as e:
        print(e, file=sys.stderr)
        exit(-1)
