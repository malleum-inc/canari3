#!/usr/bin/env python

import os
import imp
import re
from canari.maltego.configuration import MaltegoEntity
from canari.pkgutils.maltego import MaltegoDistribution, MtzDistribution

from common import canari_main, project_tree, parse_bool
from framework import SubCommand, Argument
from canari.maltego.entities import Entity


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.5'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def parse_args(args):
    if args.outfile is None:
        try:
            args.outfile = os.path.join(project_tree()['transforms'], 'common', 'entities.py')
        except ValueError:
            args.outfile = 'entities.py'
    if args.maltego_entities:
        args.namespace.extend(args.exclude_namespace)
        args.exclude_namespace = []
    return args


def normalize_fn(fn):
    # Get rid of starting underscores or numbers and bad chars for var names in python
    return re.sub(r'[^A-Za-z0-9]', '', re.sub(r'^[^A-Za-z]+', '', fn))


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
            parse_bool('%r already exists. Are you sure you want to overwrite it?' % opts.outfile, default='n'):
        exit(-1)

    distribution = None
    if not opts.mtz_file:
        distribution = MaltegoDistribution()
        if distribution.version >= '3.4.0':
            print("""
=========================== ERROR: NOT SUPPORTED ===========================

 Starting from Maltego v3.4.0 the 'canari generate-entities' command can no
 longer generate entity definition files from the Maltego configuration
 directory. Entities can only be generated from export files (*.mtz). To
 export entities navigate to the 'Manage' tab in Maltego, then click on the
 'Export Entities' button and follow the prompts. Once the entities have
 been exported, run the following command:

 shell> canari generate-entities -m myentities.mtz

=========================== ERROR: NOT SUPPORTED ===========================
                """)
            exit(-1)
    else:
        distribution = MtzDistribution(opts.mtz_file)

    namespaces = dict()

    excluded_entities = []
    if opts.append:
        existing_entities = get_existing_entities(opts.outfile)
        # excluded_entities.extend([e._type_ for e in existing_entities])
        for entity_class in existing_entities:
            excluded_entities.extend(entity_class._type_)
            if entity_class._type_.endswith('Entity'):
                namespaces[entity_class._namespace_] = entity_class.__name__

    print('Generating %r...' % opts.outfile)
    outfile = open(opts.outfile, 'ab' if opts.append else 'wb')

    if opts.append:
        outfile.write('\n\n')
    else:
        outfile.write('#!/usr/bin/env python\n\nfrom canari.maltego.entities import EntityField, Entity\n\n\n')

    for entity_file in distribution.entity_files:
        print 'Parsing %s...' % entity_file
        entity = MaltegoEntity.parse(
            distribution.read_file(entity_file)
        )

        if (opts.entity and entity.id not in opts.entity) or entity.id in excluded_entities:
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
            base_classname = '%sEntity' % (''.join([n.title() for n in namespace_entity[:-1]]))
            namespaces[namespace] = base_classname
            outfile.write('class %s(Entity):\n    _namespace_ = %r\n\n' % (base_classname, namespace))
        else:
            base_classname = namespaces[namespace]

        for field in entity.properties.fields.itervalues():
            fields = [
                'name=%r' % field.name,
                'propname=%r' % normalize_fn(field.name),
                'displayname=%r' % field.displayname

            ]
            outfile.write('@EntityField(%s)\n' % ', '.join(fields))

        outfile.write('class %s(%s):\n    pass\n\n\n' % (classname, base_classname))

    outfile.close()
    print 'done.'