import os
import click

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.3'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'


def create_profile(config_dir, project, transform_package):
    try:
        mtz_dir = os.getcwd()

        if project.is_valid and project.name == transform_package.name:
            mtz_dir = project.root_dir

        transform_package.create_profile(config_dir, mtz_dir)
    except ValueError as e:
        click.echo(str(e), err=True)
        exit(-1)
