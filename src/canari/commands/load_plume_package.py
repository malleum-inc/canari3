from __future__ import print_function

import os
import sys

from canari.commands.common import canari_main
from canari.commands.framework import SubCommand, Argument
from canari.pkgutils.transform import TransformDistribution
from canari.utils.fs import PushDir

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.6'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


# Dictionary of detected transforms
transforms = {}


# Main
@SubCommand(
    canari_main,
    help="Loads a canari package into Plume.",
    description="Loads a canari package into Plume."
)
@Argument(
    'package',
    metavar='<package>',
    help='the name of the canari transforms package to load into Plume.'
)
@Argument(
    '-d',
    '--plume-dir',
    metavar='[www dir]',
    default=os.getcwd(),
    help='the path where Plume is installed.'
)
@Argument(
        '--accept-defaults',
        '-y',
        help='Load Plume package with all the defaults in non-interactive mode.',
        default=False,
        action='store_true'
)
def load_plume_package(opts):

    with PushDir(opts.plume_dir):
        if not os.path.exists('canari.conf'):
            print('Plume does not appear to be installed in %s.' % opts.plume_dir, file=sys.stderr)
            print("Please run 'canari install-plume' and try again.", file=sys.stderr)
            exit(-1)

        transform_package = None
        try:
            transform_package = TransformDistribution(opts.package)
        except ValueError as e:
            print('An error occurred', e, file=sys.stderr)
            exit(-1)

        if transform_package.has_remote_transforms:
            try:
                transform_package.configure(opts.plume_dir, remote=True, defaults=opts.accept_defaults)
            except ImportError as e:
                print('An error occurred while trying to import %r from %s: %s' % (
                    transform_package.name, opts.plume_dir, e
                ), file=sys.stderr)
                print('Please make sure that %r is importable from %s' % (transform_package.name, opts.plume_dir),
                      file=sys.stderr)
                exit(-1)
            print('Please restart plume for changes to take effect.', file=sys.stderr)
            exit(0)

    print('Error: no remote transforms found. '
          'Please make sure that at least one transform has remote=True set before retrying.', file=sys.stderr)
    exit(-1)
