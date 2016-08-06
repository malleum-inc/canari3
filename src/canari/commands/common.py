import os
import re
import sys
import pwd
import unicodedata

from argparse import Action

from canari.commands.framework import Command
from canari.config import load_config, OPTION_LOCAL_PATH

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class ParseFieldsAction(Action):
    """
    Custom argparse action to parse arguments for the run- and debug-transform commands. This ensures that all
    positional arguments are parsed and stored correctly.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        # Does the value argument have an equals ('=') sign that is not escaped and is the params argument populated?
        if namespace.params and re.search(r'(?<=[^\\])=', namespace.value):
            # if so, apply fix and pop last element of namespace.params into namespace.value
            # and copy what was in namespace.value into namespace.fields to fix everything
            values = namespace.value
            namespace.value = namespace.params.pop().replace('\=', '=')
            namespace.fields = values
            # Next parse our fields argument into a dictionary
            fields = re.split(r'(?<=[^\\])#', values)
            if fields:
                namespace.fields = dict(
                    map(
                        lambda x: [
                            field.replace('\#', '#').replace('\=', '=').replace('\\\\', '\\')
                            for field in re.split(r'(?<=[^\\])=', x, 1)
                        ],
                        fields
                    )
                )


@Command(description='Centralized Canari Management System')
def canari_main(opts):
    """
    This is the main function for the Canari commander. Nothing special here.
    """
    profile_dir = os.path.join(os.path.expanduser('~'), '.canari')
    if not os.path.lexists(profile_dir):
        os.makedirs(profile_dir)
    fix_pypath()
    fix_binpath(load_config()[OPTION_LOCAL_PATH])
    opts.command_function(opts)


def to_utf8(s):
    return unicodedata.normalize('NFKD', unicode(s)).encode('ascii', 'ignore')


def getlogin():
    try:
        return os.getlogin()
    except:
        return pwd.getpwuid(os.getuid())[0]


def uproot():
    if os.name == 'posix' and not os.geteuid():
        login = getlogin()

        if login != 'root':
            print 'Why are you using root to run this command? You should be using %s! Bringing you down...' % login
            user = pwd.getpwnam(login)
            os.setgid(user.pw_gid)
            os.setuid(user.pw_uid)


def fix_pypath():
    if '' not in sys.path:
        sys.path.insert(0, '')


def fix_binpath(paths):
    if paths is not None and paths:
        if isinstance(paths, basestring):
            os.environ['PATH'] = paths
        elif isinstance(paths, list):
            os.environ['PATH'] = os.pathsep.join(paths)


