import logging
import os
import re
import sys
import ssl
import unicodedata

from argparse import Action

from canari.commands.framework import Command
from canari.config import load_config, OPTION_LOCAL_PATH
from canari.mode import is_local_exec_mode

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = [
    'https://dnaeon.github.io/disable-python-ssl-verification/'
]

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


logger = logging.getLogger(__name__)


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


def init_logging():
    config = load_config()
    section = 'canari.%s.logging_' % ('local' if is_local_exec_mode() else 'remote')
    logging.basicConfig(
            level=config['%slevel' % section],
            format=config['%sformat' % section],
            datefmt=config['%sdatefmt' % section])


def init_ssl_verification():

    mode = 'local' if is_local_exec_mode() else 'remote'
    disable_ssl = not load_config()['canari.%s.verify_ssl_certs' % mode]

    logger.debug("SSL certificate verification is %s for %s transforms", 'disabled' if disable_ssl else 'enabled', mode)
    if disable_ssl:
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            # Legacy Python that doesn't verify HTTPS certificates by default
            pass
        else:
            # Handle target environment that doesn't support HTTPS verification
            ssl._create_default_https_context = _create_unverified_https_context


@Command(description='Centralized Canari Management System')
def canari_main(opts):
    """
    This is the main function for the Canari commander. Nothing special here.
    """
    init_logging()
    init_ssl_verification()
    profile_dir = os.path.join(os.path.expanduser('~'), '.canari')
    if not os.path.lexists(profile_dir):
        os.makedirs(profile_dir)
    fix_pypath()
    fix_binpath(load_config()[OPTION_LOCAL_PATH])
    opts.command_function(opts)


def to_utf8(s):
    return unicodedata.normalize('NFKD', unicode(s)).encode('ascii', 'ignore')


def uproot():
    if os.name == 'posix' and not os.geteuid():
        login = os.getlogin()

        if login != 'root':
            print 'Why are you using root to run this command? You should be using %s! Bringing you down...' % login
            import pwd

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


