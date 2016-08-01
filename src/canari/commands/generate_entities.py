#!/usr/bin/env python
import keyword
import os
import re

from mrbob.configurator import Configurator
from mrbob.rendering import jinja2_env

from canari.maltego.configuration import MaltegoEntity
from canari.maltego.message import Entity, StringEntityField
from canari.pkgutils.maltego import MtzDistribution
from canari.project import CanariProject
from canari.question import parse_bool
from common import canari_main
from framework import SubCommand, Argument

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPLv3'
__version__ = '0.5'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
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


def parse_args(args):
    project = CanariProject(args.out_path)

    if project.is_valid:
        args.out_path = project.common_dir
        args.out_file = project.entities_py
    else:
        args.out_path = project.root_dir
        args.out_file = os.path.join(args.out_path, 'entities.py')

    if os.path.exists(args.out_file) and not args.append and not \
            parse_bool('%r already exists. Are you sure you want to overwrite it?' % args.out_file, default=False):
        exit(-1)

    if not args.mtz_file:
        if not project.is_valid or not os.path.lexists(project.entities_mtz):
            print("Please specify a valid MTZ file.")
            exit(-1)
        args.mtz_file = project.entities_mtz

    if args.maltego_entities:
        args.namespace.extend(args.exclude_namespace)
        args.exclude_namespace = []

    args.project = project

    return args


def normalize_fn(fn):
    # Get rid of starting underscores or numbers and bad chars for var names in python
    return re.sub(r'[^A-Za-z0-9]+', '_', re.sub(r'^[^A-Za-z]+', '', fn))



@SubCommand(
    canari_main,
    help='Converts Maltego entity definition files to Canari python classes. Excludes Maltego built-in entities by '
         'default.',
    description='Converts Maltego entity definition files to Canari python classes. Excludes Maltego built-in entities '
                'by default.'
)
@Argument(
    'out_path',
    metavar='[output path]',
    help='Which path to write the output to.',
    default=os.getcwd(),
    nargs='?'
)
@Argument(
    '--mtz-file',
    '-m',
    metavar='<mtzfile>',
    help='A *.mtz file containing an export of Maltego entities.',
    required=False
)
@Argument(
    '--exclude-namespace',
    '-e',
    metavar='<namespace>',
    help='Name of Maltego entity namespace to ignore. Can be defined multiple times.',
    required=False,
    action='append',
    default=['maltego', 'maltego.affiliation']
)
@Argument(
    '--namespace',
    '-n',
    metavar='<namespace>',
    help='Name of Maltego entity namespace to generate entity classes for. Can be defined multiple times.',
    required=False,
    action='append',
    default=[]
)
@Argument(
    '--maltego-entities',
    '-M',
    help="Generate entities belonging to the 'maltego' namespace.",
    default=False,
    action='store_true'
)
@Argument(
    '--append',
    '-a',
    help='Whether or not to append to the existing *.py file.',
    action='store_true',
    default=False
)
@Argument(
    '--entity',
    '-E',
    metavar='<entity>',
    help='Name of Maltego entity to generate Canari python class for.',
    required=False,
    action='append',
    default=[]
)
def generate_entities(args):
    opts = parse_args(args)

    mtz = MtzDistribution(opts.mtz_file)
    target = opts.out_path

    variables = opts.project.configuration['variables']

    entity_definitions = {}

    matcher = re.compile('(.+)\.([^\.]+)$')

    for entity_file in mtz.entities:
        entity = MaltegoEntity.parse(mtz.read_file(entity_file))
        namespace, name = matcher.match(entity.id).groups()
        if namespace in opts.exclude_namespace:
            continue
        elif not opts.namespace or namespace in opts.namespace:
            entity_definitions[(namespace, name)] = entity

    entity_classes = []

    if opts.append:
        module = opts.project.entities_module
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
    })

    configurator = Configurator(
            'canari.resources.templates:generate_entities',
            target,
            {'non_interactive': True},
            variables=variables
    )

    configurator.ask_questions()

    print('Generating entities for %r...' % variables['project.name'])
    configurator.render()

    print('done!')


