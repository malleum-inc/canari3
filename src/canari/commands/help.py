from framework import SubCommand, Argument
from common import canari_main


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


@SubCommand(
    canari_main,
    help='Shows help related to various canari commands',
    description='Shows help related to various canari commands'
)
@Argument(
    'command',
    metavar='<command>',
    choices=canari_main.subparsers.choices,
    default='help',
    nargs='?',
    help='The canari command you want help for.'
)
def help(opts):
    canari_main.subparsers.choices[opts.command].print_help()