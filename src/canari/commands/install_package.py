#!/usr/bin/env python

import os
from canari.pkgutils.transform import TransformDistribution

from common import canari_main, uproot
from canari.utils.fs import pushd
from framework import SubCommand, Argument


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.6'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


# Extra sauce to parse args
def parse_args(args):
    uproot()
    if args.settings_dir:
        args.settings_dir = os.path.realpath(args.settings_dir)
    return args


# Argument parser
@SubCommand(
    canari_main,
    help="Installs and configures canari transform packages in Maltego's UI",
    description="Installs and configures canari transform packages in Maltego's UI"
)
@Argument(
    'package',
    metavar='<package>',
    help='the name of the canari transforms package to install.'
)
@Argument(
    '-w',
    '--working-dir',
    metavar='[working dir]',
    default=None,
    help="the path that will be used as the working directory for "
         "the transforms being installed (default: ~/.canari/)"
)
@Argument(
    '-s',
    '--settings-dir',
    metavar='[settings dir]',
    default=None,
    help='the path to the Maltego settings directory (automatically detected if excluded)'
)
def install_package(args):

    opts = parse_args(args)

    try:
        with pushd(opts.working_dir or os.getcwd()):
            transform_package = TransformDistribution(opts.package)
            transform_package.install(opts.working_dir, opts.settings_dir)
    except ValueError, e:
        print str(e)
        exit(-1)