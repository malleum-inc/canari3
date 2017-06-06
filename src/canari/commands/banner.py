from common import canari_main
from framework import SubCommand


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
    help='Show banner of Canari framework that is currently active.',
    description='Show banner of Canari framework that is currently active.'
)
def banner(args):
    print r"""
    Your running ...
                                 _     ___ 
         _______ ____  ___ _____(_)   /_  /
        / __/ _ `/ _ \/ _ `/ __/ /   /_  /
        \__/\_,_/_//_/\_,_/_/ /_/   /___/

                                            ... http://github.com/redcanari/canari3
    """