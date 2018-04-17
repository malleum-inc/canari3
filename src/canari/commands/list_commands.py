from __future__ import print_function

import sys

from canari.commands.common import canari_main
from canari.maltego.utils import highlight
from canari.commands.framework import SubCommand

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
    for name, cmd in sorted(cmds.items()):
        print('%s - %s' % (highlight(name, 'green', True), cmd.description), file=sys.stderr)
