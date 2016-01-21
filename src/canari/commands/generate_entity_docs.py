#!/usr/bin/env python

import os
import imp
import inspect
import tokenize
import StringIO

from mrbob.configurator import Configurator

import canari
from canari.maltego.configuration import MaltegoEntity
from canari.pkgutils.maltego import MtzDistribution
from canari.maltego.message import Entity
from common import canari_main, project_tree, parse_bool
from framework import SubCommand, Argument


__author__ = 'Tomas Lima'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = ['Tomas Lima']

__license__ = 'GPLv3'
__version__ = '0.5'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


@SubCommand(
    canari_main,
    help='Create entities documentation from Canari python classes file.',
    description='Create entities documentation from Canari python classes file.'
)
@Argument(
    '--entities-filepath',
    '-e',
    metavar='<entities.py>',
    help='A entities.py file containing the Canari python classes.',
    default='entities.py',
    required=False
)
@Argument(
    '--doc-filepath',
    '-d',
    metavar='<entities.rst>',
    help='A filename (.rst) where documentation will be written.',
    default='entities.rst',
    required=True
)
@Argument(
    '--transform-package',
    '-t',
    metavar='<sploitego>',
    help='A transform package name already installed on system.',
    required=False
)
def generate_entity_docs(args):
    opts = parse_args(args)

    entities_module = load_entities_module(opts.entities_filepath)

    entities = collect_entities_information(entities_module)

    #rst_content = generate_doc(entities)
    new_generate_doc(entities, opts.doc_filepath)

    #with open(opts.doc_filepath, 'w') as fp:
    #    fp.write(rst_content)

    print "Documentation file completed: %s" % opts.doc_filepath


def parse_args(args):
    if args.transform_package:
        module_path = imp.find_module(args.transform_package)[1]
        args.entities_filepath = os.path.join(module_path, 'transforms', 'common', 'entities.py')
    elif not args.entities_filepath:
        try:
            args.entities_filepath = os.path.join(project_tree()['transforms'], 'common', 'entities.py')
        except ValueError:
            args.entities_filepath = 'entities.py'

    return args


def load_entities_module(filepath):
    module_name, _ = os.path.splitext(os.path.split(filepath)[-1])
    entities_module = imp.load_source(module_name, filepath)
    return entities_module


def sanitize(raw_str):
    strio = StringIO.StringIO(raw_str)
    tokens = tokenize.generate_tokens(strio.readline)
    return tokenize.untokenize(tokens)


def collect_entities_information(entities_module):
    entities = list()

    for entity_name, entity_object in inspect.getmembers(entities_module):
        if entity_name == "__all__":
            entities_list = entity_object

    for entity_name, entity_object in inspect.getmembers(entities_module):

        if not inspect.isclass(entity_object):
            continue

        if entity_name not in entities_list:
            continue

        entity = dict()
        entity['class'] = sanitize(entity_name)
        entity['superclass'] = sanitize(str(inspect.getmro(entity_object)[1]).split('.')[-1][:-2])
        entity['parameters'] = list()

        if '_alias_' in entity_object.__dict__:
            if entity_object.__dict__['_alias_'] != entity_name:
                entity['alias'] = sanitize(entity_object.__dict__['_alias_'])

        for param_key, param_value in entity_object.__dict__.iteritems():
            if param_key.startswith('_'):
                continue

            if not hasattr(param_value, 'display_name'):
                continue

            parameter = dict()
            # Display Name
            parameter['display_name'] = sanitize(param_value.display_name)
            # Type
            parameter['type'] = sanitize(str(param_value.__class__).split('.')[-1][:-2])
            # Canary Property
            parameter['canari'] = sanitize(param_key)
            # Maltego Property
            parameter['maltego'] = sanitize(param_value.name)
            # Main Property
            parameter['is_value'] = sanitize(param_value.is_value)

            entity['parameters'].append(parameter)

        entity['parameters'] = sorted(entity['parameters'], key=lambda k: k['canari'])
        entities.append(entity)

    entities = sorted(entities, key=lambda k: k['class'])
    return entities


def new_generate_doc(entities, output_file):

    TEMPLATE_ENTITY_DATA = '''\n\n-------------\n\n\n\n\n%s\n
    * Class: ``%s``
    * Inherits from: ``%s``
    * Class alias: ``%s``
    '''

    TEMPLATE_ENTITY_TABLE_HEADER = '''
    **Parameters**\n
    .. csv-table::
    \t:header: Display Name,Type,Canari Property,Maltego Property,Main Property
    '''

    TEMPLATE_ENTITY_TABLE_DATA = '''\n\t%s,%s,``%s``,``%s``,%s'''

    rst_content = ""
    for entity in entities:

        entity_class = entity['class'] if 'class' in entity else '-'
        entity_superclass = entity['superclass'] if 'superclass' in entity else '-'
        entity_aliasclass = entity['alias'] if 'alias' in entity else '-'

        rst_content += TEMPLATE_ENTITY_DATA % (
                    entity_class + "\n" + "-" * len(entity_class),
                    entity_class,
                    entity_superclass,
                    entity_aliasclass
                   )

        if entity['parameters']:
            rst_content += TEMPLATE_ENTITY_TABLE_HEADER

            for parameter in entity['parameters']:
                p_dname = parameter['display_name'] if 'display_name' in parameter else '-'
                p_type = parameter['type'] if 'type' in parameter else '-'
                p_canari = parameter['canari'] if 'canari' in parameter else '-'
                p_maltego = parameter['maltego'] if 'maltego' in parameter else '-'
                p_isvalue = "Yes" if parameter['is_value'] == "True" else "No"

                rst_content += TEMPLATE_ENTITY_TABLE_DATA % (
                    p_dname, p_type, p_canari, p_maltego, p_isvalue)

    variables = {
        'doc.author.name': canari.__author__,
        'doc.author.name': canari.__author__,
        'doc.author.email': canari.__email__,
        'doc.version': canari.__version__,
        'doc.title': 'Maltego Entities (FIXME)',
        'entities.content': rst_content
    }

    if os.path.exists(output_file):
        print('A file with the name %s already exists... exiting' % output_file)
        exit(-1)

    print('Creating documentation in %s' % output_file)
    configurator = Configurator(template='canari.resources.templates:generate_entity_docs',
                                target_directory=output_file,
                                bobconfig={'non_interactive': False, 'remember_answers': True},
                                variables=variables
                               )

    configurator.ask_questions()
    configurator.render()


def generate_doc(entities):



    return rst_content
