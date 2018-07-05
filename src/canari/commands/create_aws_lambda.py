from __future__ import print_function

import sys
import os

from pkg_resources import get_distribution

if sys.version_info[0] > 2:
    from queue import Queue
else:
    from Queue import Queue

from mrbob.configurator import Configurator

from canari.commands.common import canari_main
from canari.commands.framework import SubCommand, Argument
from canari.pkgutils.transform import TransformDistribution
from canari.project import CanariProject
from canari.utils.fs import PushDir
__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


BLACKLISTED_REQUIREMENTS = [
    'mr.bob',
    'argparse',
    'flask',
    'Twisted',
    'pyopenssl',
    'service_identity',
    'pyasn1',
    'boto3'
]


# Queue for blocking until we get a result from hook to setup(). Ugly but effective :P
q = Queue()


def setup_hook(**kwargs):
    print("Gathering package requirements for %s..." % kwargs['name'], file=sys.stderr)
    q.put(([r for r in kwargs.get('install_requires', []) if not r.startswith('canari')]))


def hook_setup():
    import setuptools
    setuptools.setup = setup_hook


def blacklisted(requirement):
    for b in BLACKLISTED_REQUIREMENTS:
        if b == requirement.name:
            return True
    return False


def get_dependencies(project):
    with PushDir(project.root_dir):
        hook_setup()
        import setup
    dependencies = set([str(r) for r in get_distribution('canari').requires() if not blacklisted(r)])
    return dependencies.union(q.get())


# Argument parser
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
    '--region',
    metavar='<AWS region>',
    help="The region to store the S3 objects in"
)
def create_aws_lambda(opts):
    try:
        project = CanariProject()
        target = os.path.join(project.root_dir, 'aws')

        with PushDir(project.src_dir):
            transform_package = TransformDistribution(project.name)
            variables = {
                'project.name': project.name,
                'project.requirements': get_dependencies(project),
                'package.transforms': [t() for t in transform_package.transforms]
            }

            configurator = Configurator(
                'canari.resources.templates:create_aws_lambda',
                target,
                {'non_interactive': True},
                variables=variables
            )

            configurator.ask_questions()

            print('Generating Chalice project for %r in %r...' % (project.name, target), file=sys.stderr)
            configurator.render()

            transform_package.configure(os.path.join(target, 'chalicelib'), remote=True)

            print("To deploy type 'chalice deploy' in the %r directory" % target)
            print('done!', file=sys.stderr)
    except ValueError as e:
        print(e, file=sys.stderr)
        exit(-1)
