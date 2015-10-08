# !/usr/bin/env python

import os
from canari.pkgutils.transform import TransformDistribution

from common import canari_main
from framework import SubCommand, Argument


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.4'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def parse_args(args):
    if args.settings_dir:
        args.settings_dir = os.path.realpath(args.settings_dir)
    return args


@SubCommand(
    canari_main,
    help="Uninstalls and unconfigures canari transform packages in Maltego's UI.",
    description="Uninstalls and unconfigures canari transform packages in Maltego's UI."
)
@Argument(
    'package',
    metavar='<package>',
    help='the name of the canari transforms package to uninstall.'
)
@Argument(
    '-s',
    '--settings-dir',
    metavar='[settings dir]',
    default=None,
    help='the path to the Maltego settings directory (automatically detected if excluded)'
)
@Argument(
    '-w',
    '--working-dir',
    metavar='[working dir]',
    default=None,
    help="the path that will be used as the working directory for "
         "the transforms being uninstalled (default: ~/.canari/)"
)
def uninstall_package(args):
    opts = parse_args(args)

    try:
        transform_package = TransformDistribution(opts.package)
        transform_package.uninstall(opts.working_dir, opts.settings_dir)
    except ValueError, e:
        print str(e)
        exit(-1)
