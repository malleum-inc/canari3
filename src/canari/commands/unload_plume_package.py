import os

import click

from canari.utils.fs import PushDir

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.6'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'


def unload_plume_package(package, plume_dir):
    with PushDir(plume_dir):
        if not os.path.exists('canari.conf'):
            click.echo('Plume does not appear to be installed in %s.' % plume_dir, err=True)
            click.echo("Please run 'canari install-plume' and try again.", err=True)
            exit(-1)
        try:
            package.configure(plume_dir, load=False, remote=True)
        except ImportError:
            pass

    exit(0)
