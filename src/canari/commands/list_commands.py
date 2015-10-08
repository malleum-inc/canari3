#!/usr/bin/env python

from common import canari_main
from canari.maltego.utils import highlight
from framework import SubCommand

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.7'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


@SubCommand(
    canari_main,
    help='Lists all the available canari commands.',
    description='Lists all the available canari commands.'
)
def list_commands(opts):
    cmds = canari_main.subparsers.choices
    for name, cmd in sorted(cmds.iteritems()):
        print ('%s - %s' % (highlight(name, 'green', True), cmd.description))