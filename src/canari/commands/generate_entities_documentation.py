#!/usr/bin/env python

import os
import imp
import inspect

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

def parse_args(args):
    if not args.entities_filepath:
        try:
            args.entities_filepath = os.path.join(project_tree()['transforms'], 'common', 'entities.py')
        except ValueError:
            args.entities_filepath = 'entities.py'

    if not args.doc_filepath:
        args.doc_filepath = 'entities.rst'

    return args

def load_entities_module(filepath):
    module_name, _ = os.path.splitext(os.path.split(filepath)[-1])
    entities_module = imp.load_source(module_name, filepath)
    return entities_module

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
    required=False
)
@Argument(
    '--doc-filepath',
    '-d',
    metavar='<entities.rst>',
    help='A filename (.rst) where documentation will be written.',
    required=True
)
def generate_entities_documentation(args):
    opts = parse_args(args)
    
    entities_module = load_entities_module(opts.entities_filepath)

    entities = collect_entities_information(entities_module)

    rst_content = generate_doc(entities)

    with open(opts.doc_filepath, 'w') as fp:
        fp.write(rst_content)

    print "Documentatio file completed: %s" % opts.doc_filepath

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
        entity['class'] = entity_name
        entity['superclass'] = str(inspect.getmro(entity_object)[1]).split('.')[-1][:-2]
        entity['parameters'] = list()

        if '_alias_' in entity_object.__dict__:
            if entity_object.__dict__['_alias_'] != entity_name:
                entity['alias'] = entity_object.__dict__['_alias_']

        for param_key, param_value in entity_object.__dict__.iteritems():
            if param_key.startswith('_'):
                continue

            if not hasattr(param_value, 'display_name'):
                continue

            parameter = dict()
            # Display Name
            parameter['display_name'] = param_value.display_name
            # Type
            parameter['type'] = str(param_value.__class__).split('.')[-1][:-2]
            # Canary Property
            parameter['canari'] = param_key
            # Maltego Property
            parameter['maltego'] = param_value.name
            # Main Property
            parameter['is_value'] = param_value.is_value

            entity['parameters'].append(parameter)

        entity['parameters'] = sorted(entity['parameters'], key=lambda k: k['canari'])
        entities.append(entity)

    entities = sorted(entities, key=lambda k: k['class'])
    return entities



TEMPLATE_HEADER = '''
Maltego Entities
===============================================================

.. moduleauthor:: xxx xxx <xxx@xxx.com>
.. sectionauthor:: xxx xxx <xxx@xxx.com>

.. versionadded:: 3.0

'''

TEMPLATE_ENTITY_TITLE = '''\n\n-------------\n\n\n\n\n%s'''

TEMPLATE_ENTITY_DATA = '''

* Class: ``%s``
* Inherits from: ``%s``
* Class alias: ``%s``
'''

TEMPLATE_ENTITY_TABLE_HEADER = '''
**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property
'''

TEMPLATE_ENTITY_TABLE_DATA = '''\n    %s,%s,``%s``,``%s``,%s'''


def generate_doc(entities):

    rst_content = TEMPLATE_HEADER
    for entity in entities:

        entity_class = entity['class'] if 'class' in entity else '-'
        entity_superclass = entity['superclass'] if 'superclass' in entity else '-'
        entity_aliasclass = entity['alias'] if 'alias' in entity else '-'

        rst_content += TEMPLATE_ENTITY_TITLE % entity_class + "\n" + "-" * len(entity_class) 

        rst_content += TEMPLATE_ENTITY_DATA % (entity_class, entity_superclass, entity_aliasclass)

        if entity['parameters']:
            rst_content += TEMPLATE_ENTITY_TABLE_HEADER

            for parameter in entity['parameters']:
                p_dname = parameter['display_name'] if 'display_name' in parameter else '-'
                p_type = parameter['type'] if 'type' in parameter else '-'
                p_canari = parameter['canari'] if 'canari' in parameter else '-'
                p_maltego = parameter['maltego'] if 'maltego' in parameter else '-'
                p_isvalue = "Yes" if parameter['is_value'] else "No"

                rst_content += TEMPLATE_ENTITY_TABLE_DATA % (
                                p_dname, p_type, p_canari, p_maltego, p_isvalue)

    return rst_content

