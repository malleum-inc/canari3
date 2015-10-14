#!/usr/bin/env python

import os
import imp
import re

from canari.maltego.configuration import MaltegoEntity
from canari.pkgutils.maltego import MtzDistribution
from common import canari_main, project_tree, parse_bool
from framework import SubCommand, Argument
from canari.maltego.message import Entity

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
    if not args.outfile:
        try:
            args.outfile = os.path.join(project_tree()['transforms'], 'common', 'entities.py')
        except ValueError:
            args.outfile = 'entities.py'
    if not args.mtz_file:
        args.mtz_file = os.path.join(project_tree()['resources'], 'maltego', 'entities.mtz')
    if args.maltego_entities:
        args.namespace.extend(args.exclude_namespace)
        args.exclude_namespace = []
    return args


def normalize_fn(fn):
    # Get rid of starting underscores or numbers and bad chars for var names in python
    return re.sub(r'[^A-Za-z0-9]+', '_', re.sub(r'^[^A-Za-z]+', '', fn))


def get_existing_entities(filename):
    m = imp.load_source('entities', filename)
    l = []
    for c in dir(m):
        try:
            entity_class = m.__dict__[c]
            if issubclass(entity_class, Entity):
                l.append(entity_class)
        except TypeError:
            pass
    return l


class DirFile(object):
    def __init__(self, path):
        self.path = path

    def namelist(self):
        l = []
        for base, dirs, files in os.walk(self.path):
            l.extend([os.path.join(base, f) for f in files])
        return l

    def open(self, fname):
        return file(fname)


@SubCommand(
    canari_main,
    help='Converts Maltego entity definition files to Canari python classes. Excludes Maltego built-in entities by '
         'default.',
    description='Converts Maltego entity definition files to Canari python classes. Excludes Maltego built-in entities '
                'by default.'
)
@Argument(
    'outfile',
    metavar='[output file]',
    help='Which file to write the output to.',
    default=None,
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

    if os.path.exists(opts.outfile) and not opts.append and not \
            parse_bool('%r already exists. Are you sure you want to overwrite it?' % opts.outfile, default=False):
        exit(-1)

    distribution = MtzDistribution(opts.mtz_file)

    namespaces = dict()

    excluded_entities = []
    if opts.append:
        existing_entities = get_existing_entities(opts.outfile)
        for entity_class in existing_entities:
            if entity_class is Entity:
                continue
            excluded_entities.append(entity_class._type_)
            if entity_class._type_.endswith('Entity'):
                namespaces[entity_class._namespace_] = entity_class.__name__
        print 'Discovered %d existing entities, and %d namespaces...' % (len(excluded_entities), len(namespaces))
        print('Appending to %r...' % opts.outfile)
    else:
        print('Generating %r...' % opts.outfile)

    data = ''

    if opts.append:
        with open(opts.outfile) as f:
            data = f.read().strip('\n')

    outfile = open(opts.outfile, 'wb')

    if data:
        outfile.write(data + '\n\n')
    else:
        outfile.write('from canari.maltego.message import *\n\n')

    for entity_file in distribution.entity_files:
        print 'Parsing entity definition %s...' % entity_file
        entity = MaltegoEntity.parse(
            distribution.read_file(entity_file)
        )

        if (opts.entity and entity.id not in opts.entity) or entity.id in excluded_entities:
            print 'Skipping entity generation for %s as it already exists...' % entity.id
            continue

        namespace_entity = entity.id.split('.')

        base_classname = None
        namespace = '.'.join(namespace_entity[:-1])
        name = namespace_entity[-1]
        classname = name

        if (opts.namespace and namespace not in opts.namespace) or namespace in opts.exclude_namespace:
            continue

        print 'Generating entity definition for %s...' % entity_file
        if namespace not in namespaces:
            base_classname = '%sBaseEntity' % (''.join([n.title() for n in namespace_entity[:-1]]))
            namespaces[namespace] = base_classname
            outfile.write('class %s(Entity):\n    _namespace_ = %r\n\n' % (base_classname, namespace))
        else:
            base_classname = namespaces[namespace]

        outfile.write('\nclass %s(%s):\n' % (classname, base_classname))
        for field in entity.properties.fields.itervalues():
            fields = [
                'name=%r' % field.name,
                'displayname=%r' % field.displayname
            ]
            outfile.write('    %s = %s(%s)\n' % (
                normalize_fn(field.name),
                type_mapping.get(field.type, 'StringEntityField'),
                ', '.join(fields)
            ))
        outfile.write('\n')

    outfile.close()
    print 'done.'
