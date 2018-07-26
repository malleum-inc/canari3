import sys

import click

import canari

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.3'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'


def version():
    click.echo('Canari Framework v%s' % canari.version)
    click.echo('Running on Python %s (%s)' % (sys.version, sys.executable))
