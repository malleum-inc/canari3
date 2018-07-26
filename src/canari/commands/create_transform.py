import os

import click
import stringcase
from mrbob.configurator import Configurator
from mrbob.parsing import parse_config

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.4'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'


def create_transform(project, module_name):

    transform_name = stringcase.pascalcase(module_name)
    module_name = module_name.lower()

    target = project.root_dir
    transform_directory = project.transforms_dir

    if os.path.exists(os.path.join(transform_directory, '%s.py' % module_name)):
        click.echo('Transform %r already exists... quitting' % module_name, err=True)
        exit(-1)

    variables = parse_config(os.path.join(target, '.mrbob.ini'))['variables']

    variables.update({'transform.module': module_name, 'transform.name': transform_name})

    configurator = Configurator(
        'canari.resources.templates:create_transform',
        target,
        {'non_interactive': True},
        variables=variables
    )

    configurator.ask_questions()

    click.echo('Creating transform %r...' % module_name, err=True)
    configurator.render()

    click.echo('done!', err=True)
