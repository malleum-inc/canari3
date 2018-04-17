from __future__ import print_function

import os
import sys

from canari.pkgutils.transform import TransformDistribution
from canari.utils.fs import PushDir

from canari.commands.common import canari_main
from canari.commands.framework import SubCommand, Argument


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.6'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


@SubCommand(
    canari_main,
    help="Unloads a canari package from Plume.",
    description="Unloads a canari package from Plume."
)
@Argument(
    'package',
    metavar='<package>',
    help='the name of the canari transforms package to unload from Plume.'
)
@Argument(
    '-d',
    '--plume-dir',
    metavar='[www dir]',
    default=os.getcwd(),
    help='the path where Plume is installed.'
)
def unload_plume_package(opts):
    with PushDir(opts.plume_dir):
        if not os.path.exists('canari.conf'):
            print('Plume does not appear to be installed in %s.' % opts.plume_dir, file=sys.stderr)
            print("Please run 'canari install-plume' and try again.", file=sys.stderr)
            exit(-1)
        try:
            TransformDistribution(opts.package).configure(opts.plume_dir, load=False, remote=True)
        except ImportError:
            pass

    exit(0)