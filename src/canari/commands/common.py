from __future__ import print_function

import os
import sys
from getpass import getuser

from six import string_types

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'


def uproot():
    if os.name == 'posix' and not os.geteuid():
        login = getuser()

        if login != 'root':
            import pwd
            print('Why are you using root to run this command? You should be using %s! Bringing you down...' % login,
                  file=sys.stderr)
            user = pwd.getpwnam(login)
            os.setgid(user.pw_gid)
            os.setuid(user.pw_uid)


def fix_pypath():
    if '' not in sys.path:
        sys.path.insert(0, '')


def fix_binpath(paths):
    if paths is not None and paths:
        if isinstance(paths, string_types):
            os.environ['PATH'] = paths
        elif isinstance(paths, list):
            os.environ['PATH'] = os.pathsep.join(paths)
