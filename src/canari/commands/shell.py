import os
import sys
from atexit import register
from code import InteractiveConsole

import click

import canari
from canari.config import load_config
from canari.maltego.runner import scriptable_transform_runner
from canari.maltego.utils import highlight
from canari.utils.fs import PushDir

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.5'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'


def do_sudo():
    click.echo(highlight("Need to be root to run this transform... sudo'ing...", 'green', True), err=True)
    sys.argv.insert(0, 'sudo')
    os.execvp(sys.argv[0], sys.argv)


class ShellCommand(object):

    def __init__(self, transform, config):
        self.transform = transform
        self.config = config

    def __call__(self, value, *args, **kwargs):
        if os.name == 'posix' and self.transform.superuser and os.geteuid():
            do_sudo()
        if args and isinstance(args[0], dict):
            kwargs.update(args[0])
            args = args[1:]
        return scriptable_transform_runner(self.transform, value, kwargs, list(args), self.config)


class MtgConsole(InteractiveConsole):

    def __init__(self, transform_classes, auto_sudo=False):
        locals_ = {}
        asked = False
        config = load_config()
        for transform in transform_classes:
            locals_['do' + transform.name.split('.')[-1]] = ShellCommand(transform, config)
            if not asked and transform.superuser and os.name == 'posix' and os.geteuid():
                if not auto_sudo and click.prompt("A transform requiring 'root' access was detected."
                                                  " Would you like to run this shell as 'root'?", default=False):
                    do_sudo()
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


def shell(transform_package, working_dir, sudo):
    with PushDir(working_dir or transform_package.default_prefix):
        mtg_console = MtgConsole(transform_package.transforms, auto_sudo=sudo)
        mtg_console.interact(highlight('Welcome to Canari %s.' % canari.__version__, 'green', True))
