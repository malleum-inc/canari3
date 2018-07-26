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


# Dictionary of detected transforms
transforms = {}


def load_plume_package(transform_package, plume_dir, accept_defaults):

    with PushDir(plume_dir):
        if not os.path.exists('canari.conf'):
            click.echo('Plume does not appear to be installed in %s.' % plume_dir, err=True)
            click.echo("Please run 'canari install-plume' and try again.", err=True)
            exit(-1)

        if transform_package.has_remote_transforms:
            try:
                transform_package.configure(plume_dir, remote=True, defaults=accept_defaults)
            except ImportError as e:
                click.echo('An error occurred while trying to import %r from %s: %s' % (
                    transform_package.name, plume_dir, e
                ), err=True)
                click.echo('Please make sure that %r is importable from %s' % (transform_package.name, plume_dir),
                           err=True)
                exit(-1)
            click.echo('Please restart plume for changes to take effect.', err=True)
            exit(0)

    click.echo('Error: no remote transforms found. Please make sure that at least one transform has remote=True '
               'set before retrying.', err=True)
    exit(-1)
