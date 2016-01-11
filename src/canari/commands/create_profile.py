#!/usr/bin/env python

import os
from canari.mode import CanariMode, set_canari_mode

from canari.pkgutils.transform import TransformDistribution
from common import canari_main, uproot
from canari.utils.fs import PushDir
from framework import SubCommand, Argument


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.3'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


# Extra sauce to parse args
def parse_args(args):
    uproot()
    return args


# Main
# Argument parser
@SubCommand(
    canari_main,
    help='Creates an importable Maltego profile (*.mtz) file.',
    description='Creates an importable Maltego profile (*.mtz) file.'
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
    help='the path that will be used as the working directory for the '
         'transforms being installed (default: current working directory)'
)
def create_profile(args):

    set_canari_mode(CanariMode.Local)

    opts = parse_args(args)
    current_dir = os.getcwd()
    try:
        with PushDir(opts.working_dir or current_dir):
            transform_package = TransformDistribution(opts.package)
            transform_package.create_profile(opts.working_dir, current_dir)
    except ValueError, e:
        print(str(e))
        exit(-1)