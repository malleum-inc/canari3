import os
import sys
from code import InteractiveConsole
from atexit import register

from canari.mode import CanariMode, set_canari_mode
from canari.pkgutils.transform import TransformDistribution
from common import canari_main
from canari.question import parse_bool
from canari.utils.fs import PushDir
from framework import SubCommand, Argument
from canari.config import load_config
from canari.maltego.utils import highlight
from canari.maltego.runner import scriptable_transform_runner
import canari

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.5'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def sudo():
    print highlight("Need to be root to run this transform... sudo'ing...", 'green', True)
    sys.argv.insert(0, 'sudo')
    os.execvp(sys.argv[0], sys.argv)


class ShellCommand(object):

    def __init__(self, transform, config):
        self.transform = transform
        self.config = config

    def __call__(self, value, *args, **kwargs):
        if os.name == 'posix' and self.transform.superuser and os.geteuid():
            sudo()
        if args and isinstance(args[0], dict):
            kwargs.update(args[0])
            args = args[1:]
        return scriptable_transform_runner(self.transform, value, kwargs, list(args), self.config)


class MtgConsole(InteractiveConsole):

    def __init__(self, transform_classes, auto_sudo=False):
        locals_ = {}
        asked = False
        config = load_config()
        for transform_class in transform_classes:
            transform = transform_class()
            locals_['do' + transform.name.split('.')[-1]] = ShellCommand(transform, config)
            if not asked and transform.superuser and os.name == 'posix' and os.geteuid():
                if not auto_sudo and parse_bool("A transform requiring 'root' access was detected."
                                                " Would you like to run this shell as 'root'?", False):
                    sudo()
                asked = True

        InteractiveConsole.__init__(self, locals=locals_)
        MtgConsole.init_history(os.path.expanduser('~/.mtgsh_history'))

    @staticmethod
    def init_history(history_file):
        try:
            import readline
            readline.parse_and_bind('tab: complete')
            if hasattr(readline, "read_history_file"):
                try:
                    readline.read_history_file(history_file)
                except IOError:
                    pass
                register(lambda h: readline.write_history_file(h), history_file)
        except ImportError:
            pass


@SubCommand(
    canari_main,
    help='Creates a Canari debug shell for the specified transform package.',
    description='Creates a Canari debug shell for the specified transform package.'
)
@Argument(
    'package',
    metavar='<package name>',
    help='The name of the canari package you wish to load local transform from for the Canari shell session.'
)
@Argument(
    '-w',
    '--working-dir',
    metavar='[working dir]',
    default=None,
    help="the path that will be used as the working directory for "
         "the transforms being executed in the shell (default: ~/.canari/)"
)
@Argument(
    '-s',
    '--sudo',
    action='store_true',
    default=False,
    help='Instructs the shell to automatically elevate privileges to root if necessary.'
)
def shell(opts):

    set_canari_mode(CanariMode.LocalShellDebug)

    if not opts.package.endswith('transforms'):
        opts.package = '%s.transforms' % opts.package

    try:
        transform_package = TransformDistribution(opts.package)
        with PushDir(opts.working_dir or transform_package.default_prefix):
            mtg_console = MtgConsole(transform_package.transforms, auto_sudo=opts.sudo)
            mtg_console.interact(highlight('Welcome to Canari %s.' % canari.__version__, 'green', True))
    except ValueError, e:
        print str(e)
        exit(-1)
