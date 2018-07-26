import math
import os
import shutil
import sys
import tempfile
import zipfile
from hashlib import md5
from mimetypes import guess_type

import boto3
import click
from mrbob.configurator import Configurator
from six import b
from six.moves import urllib

import canari
from canari.pkgutils.transform import TransformDistribution
from canari.resource import image_resources
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
__email__ = 'ndouba@redcanari.com'
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
    click.echo("Gathering package requirements for %s..." % kwargs['name'], err=True)
    q.put(([r for r in kwargs.get('install_requires', []) if not r.startswith('canari')]))


def hook_setup():
    import setuptools
    setuptools.setup = setup_hook


def get_dependencies(project):
    with PushDir(project.root_dir):
        hook_setup()
        # noinspection PyUnresolvedReferences
        import setup
    return set(q.get())


def download_progress(count, size, total_bytes):
    if not total_bytes or not size:
        click.echo('Downloading %s...' % DEPENDENCY_FILE_NAME)

    total_count = math.ceil(float(total_bytes)/size)
    percent_done = count / total_count
    click.echo('Downloading %s |%-20s| %.2f complete\r' % (
        DEPENDENCY_FILE_NAME,
        '#' * int(percent_done * 20),
        percent_done * 100
    ), nl=(count >= total_count), err=True)


def upload_images(project, bucket, region_name, access_key, secret_key):
    bucket = bucket or md5(b('canari-%s-transform-images' % project.name)).hexdigest()
    region = region_name or boto3.session.Session().region_name
    base_url = 'about:blank'

    with PushDir(project.src_dir):
        imgs = image_resources(project.name)

        if not imgs:
            return base_url

        click.echo('Uploading image resources to AWS S3 bucket %r' % bucket, err=True)
        s3 = boto3.client(
            's3',
            # Hard coded strings as credentials, not recommended.
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        if bucket not in [bkt['Name'].lower() for bkt in s3.list_buckets()['Buckets']]:
            click.echo('Creating S3 bucket %r because it does not exist' % bucket)
            s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': region})

        for i in imgs:
            img_name = os.path.basename(i)
            dst_path = 'static/%s' % md5(b(img_name)).hexdigest()
            click.echo('Uploading %r to %r...' % (i, dst_path))
            s3.upload_file(i, bucket, dst_path, ExtraArgs={'ContentType': guess_type(i)[0]})

        click.echo('Creating static website configuration for bucket %r...' % bucket)
        s3.put_bucket_website(Bucket=bucket, WebsiteConfiguration={'IndexDocument': {'Suffix': 'index.html'}})

        click.echo('Adjusting bucket policy for public GetObject access...')
        s3.put_bucket_policy(Bucket=bucket, Policy=S3_CDN_BUCKET_POLICY % bucket)

        base_url = 'http://%s.s3-website.%s.amazonaws.com/static/' % (bucket, region)
        click.echo('Static images are now hosted at %r!' % base_url)

    return base_url


def create_aws_lambda(project, bucket, region_name, access_key, secret_key):
    try:
        target = os.path.join(project.root_dir, 'aws')
        dot_chalice = os.path.join(target, '.chalice')
        dot_chalice_backup = None

        if os.path.lexists(dot_chalice):
            click.echo("Saving original 'aws/.chalice' ...", err=True)
            dot_chalice_backup = tempfile.mkdtemp(prefix='.chalice', suffix='.bak')
            shutil.move(dot_chalice, dot_chalice_backup)

        with PushDir(project.src_dir):
            transform_package = TransformDistribution(project.name)
            if not transform_package.remote_transforms:
                click.echo("No remote transforms found in %r... exiting" % project.name)
                exit(-1)

            cdn_base_url = upload_images(project, bucket, region_name, access_key, secret_key)

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

            click.echo('Generating Chalice project for %r in %r...' % (project.name, target), err=True)
            configurator.ask_questions()
            configurator.render()

            transform_package.configure(os.path.join(target, 'chalicelib'), remote=True, additional_options={
                'cdn': cdn_base_url
            })

            dst_dir = '../aws/vendor/%s' % project.name
            if os.path.lexists(dst_dir):
                shutil.rmtree(dst_dir)

            click.echo("Copying %r project tree to the 'aws' directory..." % project.name, err=True)
            shutil.copytree(project.name, dst_dir,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".*", "*.gif", "*.jpg", "*.jpeg",
                                                          "*.png", "*.whl", "*.mt*"))

            deps_dst = os.path.join(tempfile.gettempdir(), DEPENDENCY_FILE_NAME)
            try:
                click.echo("Copying Amazon dependencies for Canari to the 'aws/vendor' directory...", err=True)
                if not os.path.lexists(deps_dst):
                    click.echo("Downloading dependencies from %r... " % DEPENDENCY_DOWNLOAD_URL, err=True)
                    deps_dst, _ = urllib.request.urlretrieve(
                        DEPENDENCY_DOWNLOAD_URL, deps_dst, reporthook=download_progress)
                else:
                    click.echo("Using cached dependencies from %r" % deps_dst)

                click.echo("Decompressing dependencies into 'aws/vendor'", err=True)
                zip_file = zipfile.ZipFile(deps_dst, 'r')
                zip_file.extractall("../aws/vendor")
                zip_file.close()
            except IOError:
                if os.path.lexists(deps_dst):
                    os.unlink(deps_dst)
                click.echo("Failed to download dependencies from %r..." % DEPENDENCY_DOWNLOAD_URL)
                exit(-1)

        if dot_chalice_backup:
            click.echo("Restoring 'aws/.chalice' from %r..." % dot_chalice_backup, err=True)
            shutil.rmtree(dot_chalice)
            shutil.move(os.path.join(dot_chalice_backup, '.chalice'), target)

        click.echo("To deploy type 'chalice deploy' in the %r directory" % target, err=True)
        click.echo('done!', err=True)
    except ValueError as e:
        click.echo(e, err=True)
        exit(-1)
