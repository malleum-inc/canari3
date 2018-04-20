import os
import sys


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'find_pysudo',
    'find_dispatcher',
    'find_canari'
]


def find_script(name):
    ext = ''
    if sys.platform == 'win32':
        ext = '.bat'
    return os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), name + ext)


def find_dispatcher():
    return find_script('dispatcher')


def find_canari():
    return find_script('canari')


def find_pysudo():
    return find_script('pysudo')

