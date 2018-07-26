import keyword
import os
import re

import click
from mrbob.configurator import Configurator
from mrbob.rendering import jinja2_env

from canari.maltego.configuration import MaltegoEntity
from canari.maltego.message import Entity, StringEntityField
from canari.pkgutils.maltego import MtzDistribution

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPLv3'
__version__ = '0.5'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'

type_mapping = {
    'string': 'StringEntityField',
    'int': 'IntegerEntityField',
    'byte': 'IntegerEntityField',
    'char': 'IntegerEntityField',
    'boolean': 'BooleanEntityField',
    'float': 'FloatEntityField',
    'date': 'DateEntityField',
    'datetime': 'DateTimeEntityField',
    'timespan': 'TimeSpanEntityField',
    'color': 'ColorEntityField',
    'double': 'FloatEntityField'
}


def normalize_fn(fn):
    # Get rid of starting underscores or numbers and bad chars for var names in python
    return re.sub(r'[^A-Za-z0-9]+', '_', re.sub(r'^[^A-Za-z]+', '', fn))


def generate_entities(project, output_path, mtz_file, exclude_namespace, namespace, maltego_entities, append, entity):

    if not output_path:
        if project.is_valid:
            output_path = project.common_dir
        else:
            output_path = os.getcwd()

    entities_py = os.path.join(output_path, 'entities.py')

    if os.path.exists(entities_py) and not append:
        click.confirm('{!r} already exists. Are you sure you want to overwrite it?'.format(entities_py),
                      default=False, abort=True)

    if maltego_entities:
        namespace.extend(exclude_namespace)
        exclude_namespace = []

    mtz = MtzDistribution(mtz_file)
    target = output_path

    variables = project.configuration['variables']

    entity_definitions = {}

    matcher = re.compile('(.+)\.([^.]+)$')

    for entity_file in mtz.entities:
        entity = MaltegoEntity.parse(mtz.read_file(entity_file))
        namespace, name = matcher.match(entity.id).groups()
        if namespace in exclude_namespace:
            continue
        elif not namespace or namespace in namespace:
            entity_definitions[(namespace, name)] = entity

    entity_classes = []

    if append:
        module = project.entities_module
        for entity_class in dir(module):
            entity_class = getattr(module, entity_class)
            if isinstance(entity_class, type) and issubclass(entity_class, Entity) and entity_class is not Entity \
                    and (entity_class._namespace_, entity_class.__name__) not in entity_definitions:
                entity_classes.append(entity_class)

    def get_entity_field_class(v):
        if v == 'int':
            return 'IntegerEntityField'
        elif v == 'float':
            return 'FloatEntityField'
        elif v == 'boolean':
            return 'BooleanEntityField'
        elif v == 'timespan':
            return 'TimeSpanEntityField'
        elif v == 'datetime':
            return 'DateTimeEntityField'
        elif v == 'date':
            return 'DateEntityField'
        elif v == 'long':
            return 'LongEntityField'
        else:
            return 'StringEntityField'

    def get_property_name(v):
        v = v.replace('.', '_').replace('-', '_')
        return '%s_' % v if keyword.iskeyword(v) else v

    jinja2_env.filters['entity_properties'] = \
        lambda v: reversed([(p, getattr(v, p)) for p in dir(v) if isinstance(getattr(v, p), StringEntityField) and
                            not hasattr(Entity, p)])

    jinja2_env.filters['get_entity_field_class'] = get_entity_field_class

    jinja2_env.filters['get_property_name'] = get_property_name

    variables.update({
        'entity.definitions': entity_definitions,
        'entity.classes': entity_classes
    }, )

    configurator = Configurator(
            'canari.resources.templates:generate_entities',
            target,
            {'non_interactive': True},
            variables=variables
    )

    configurator.ask_questions()

    click.echo('Generating entities for %r...' % variables['project.name'], err=True)
    configurator.render()

    click.echo('done!', err=True)


