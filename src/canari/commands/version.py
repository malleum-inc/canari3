from __future__ import print_function

import sys

from canari.commands.common import canari_main
from canari.commands.framework import SubCommand

import canari


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.3'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


@SubCommand(
    canari_main,
    help='Show version of Canari framework that is currently active.',
    description='Show version of Canari framework that is currently active.'
)
def version(args):
    print('Canari Framework v%s' % canari.__version__, file=sys.stderr)
    print('Running on Python %s (%s)' % (sys.version, sys.executable))
