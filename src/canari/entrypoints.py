#!/usr/bin/env python
from __future__ import print_function
from future.builtins import bytes
from past.builtins import unicode
import sys
import six

# For some reason this function is being used in safedexml. We're going to avoid it completely.
six.u = unicode

from canari.mode import set_canari_mode, CanariMode
from canari.commands.common import canari_main
# Do not remove this line. It loads all our sub-commands into the main commander.
# noinspection PyUnresolvedReferences
from canari.commands import *

import subprocess
import getpass

from canari.utils.fs import FileMutex
from canari.easygui import passwordbox


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.2'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'main',
    'dispatcher',
    'sudo'
]


def main():
    try:
        set_canari_mode(CanariMode.LocalUnknown)
        canari_main()
    except KeyboardInterrupt:
        print('exiting...', file=sys.stderr)


def dispatcher():
    set_canari_mode(CanariMode.LocalDispatch)
    run_transform.run_transform.parser.prog = 'dispatcher'
    opts = run_transform.run_transform.parser.parse_args()
    run_transform.run_transform(opts)


def sudo():
    if not sys.argv[1:]:
        print('usage: %s <command>' % sys.argv[0], file=sys.stderr)
        exit(-1)

    # Let's try and run it right away to see what happens
    p = subprocess.Popen(['sudo', '-S'] + sys.argv[1:], stdin=subprocess.PIPE)
    p.communicate()

    # It ran!
    if not p.returncode:
        exit(0)

    # It didn't :( - let's lock this region now to avoid having multiple password boxes pop-up
    l = FileMutex('pysudo.%s.lock' % getpass.getuser())

    # Try running it again (maybe another process authenticated... why ask for a password again?)
    p = subprocess.Popen(['sudo', '-S'] + sys.argv[1:], stdin=subprocess.PIPE)
    p.communicate()

    if not p.returncode:
        l.unlock()
        exit(0)

    # No we really need to ask for a password :(
    for i in range(0, 3):
        password = passwordbox('Please enter your password.', 'sudo', '')
        if password is None:
            exit(1)

        # Try it out with a password now!
        p = subprocess.Popen(['sudo', '-S', 'true'], stdin=subprocess.PIPE)
        p.communicate(input=bytes('%s\n' % password, 'utf-8'))

        # Did it work? Yes: let's do it!
        if not p.returncode:
            l.unlock()
            p = subprocess.Popen(['sudo', '-S'] + sys.argv[1:], stdin=subprocess.PIPE)
            p.communicate(input=bytes('%s\n' % password, 'utf-8'))
            exit(p.returncode)

    exit(2)
