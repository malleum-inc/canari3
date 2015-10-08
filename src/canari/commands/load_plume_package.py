#!/usr/bin/env python

import os
from canari.pkgutils.transform import TransformDistribution

from common import canari_main, parse_bool
from framework import SubCommand, Argument


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPL'
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
def load_plume_package(opts):

    if not os.path.exists(os.path.join(opts.plume_dir, 'plume.py')):
        print('Plume does not appear to be installed in %s.' % opts.plume_dir)
        ans = parse_bool("Would you like to install it [Y/n]: ")
        if not ans:
            print 'Installation cancelled. Quitting...'
            exit(-1)
        os.system('canari install-plume --install-dir %s' % opts.plume_dir)
        opts.plume_dir = os.path.join(opts.plume_dir, 'plume')

    transform_package = None
    try:
        transform_package = TransformDistribution(opts.package)
    except ValueError:
        exit(-1)

    if transform_package.has_remote_transforms:
        try:
            transform_package.configure(opts.plume_dir, remote=True)
        except ImportError:
            pass
        print('Please restart plume (./plume.sh restart) for changes to take effect.')
        exit(0)

    print ('Error: no remote transforms found. '
           'Please make sure that at least one transform has remote=True in @configure before retrying.')
    exit(-1)
