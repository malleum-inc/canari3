import sys
import os
from distutils.spawn import find_executable

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'

__all__ = [
    'find_pysudo',
    'find_dispatcher',
    'find_canari'
]

bin_dir = os.path.dirname(sys.executable)


def find_script(name):
    exe = os.path.join(bin_dir, name)
    if not os.path.lexists(exe):
        return find_executable(name)
    return exe


def find_dispatcher():
    return find_script('dispatcher')


def find_canari():
    return find_script('canari')


def find_pysudo():
    return find_script('pysudo')
