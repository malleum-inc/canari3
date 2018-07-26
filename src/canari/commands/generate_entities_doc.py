import os

import click

from mrbob.configurator import Configurator
from mrbob.rendering import jinja2_env

from canari.maltego.message import StringEntityField, IntegerEntityField, FloatEntityField, Entity, \
    BooleanEntityField, TimeSpanEntityField, DateTimeEntityField, DateEntityField, LongEntityField

__author__ = 'Tomas Lima'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = ['Tomas Lima']

__license__ = 'GPLv3'
__version__ = '0.5'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'


def generate_entities_doc(project, out_path, transform_package):

    if not out_path:
        if project.is_valid:
            out_path = project.root_dir
        else:
            out_path = os.getcwd()

    jinja2_env.filters['entity_properties'] = \
        lambda v: reversed([(p, getattr(v, p)) for p in dir(v) if isinstance(getattr(v, p), StringEntityField) and
                            not hasattr(Entity, p)])

    def get_property_type(v):
        if isinstance(v, IntegerEntityField):
            return 'int'
        elif isinstance(v, FloatEntityField):
            return 'float'
        elif isinstance(v, BooleanEntityField):
            return 'bool'
        elif isinstance(v, TimeSpanEntityField):
            return 'timedelta'
        elif isinstance(v, DateTimeEntityField):
            return 'datetime'
        elif isinstance(v, DateEntityField):
            return 'date'
        elif isinstance(v, LongEntityField):
            return 'long'
        else:
            return 'str'

    jinja2_env.filters['get_property_type'] = get_property_type

    entity_module = 'canari.maltego.entities' if transform_package.name == 'canari' \
        else '%s.transforms.common.entities' % transform_package.name

    variables = {
        'transform.module': entity_module,
        'transform.entities': transform_package.entities,
        'transform.author': '%s <%s>' % (transform_package.author, transform_package.author_email)
    }

    configurator = Configurator(
            'canari.resources.templates:generate_entities_doc',
            out_path,
            {'non_interactive': True},
            variables=variables
    )

    configurator.ask_questions()

    click.echo('Creating entities.rst documentation for %r...' % transform_package.name, err=True)
    configurator.render()

    click.echo('done!', err=True)
