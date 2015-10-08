#!/usr/bin/env python

import os
from canari.pkgutils.transform import TransformDistribution

from common import canari_main
from framework import SubCommand, Argument


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPL'
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
    if not os.path.exists(os.path.join(opts.plume_dir, 'plume.py')):
        print('Plume does not appear to be installed in %s.' % opts.plume_dir)
        exit(-1)

    try:
        TransformDistribution(opts.package).configure(opts.plume_dir, load=False, remote=True)
    except ImportError:
        pass

    exit(0)