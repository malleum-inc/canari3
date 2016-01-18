import sys
import re
import json
import inspect
import canari.maltego.entities

filename = sys.argv[0].split('.py')[0]

entities = list()
entities_list = list()

for entity_name, entity_object in inspect.getmembers(canari.maltego.entities):
    if entity_name == "__all__":
        entities_list = entity_object

for entity_name, entity_object in inspect.getmembers(canari.maltego.entities):

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
        parameter['display_name'] = param_value.display_name  # Display Name
        parameter['type'] = str(param_value.__class__).split('.')[-1][:-2]  # Type
        parameter['canari'] = param_key  # Canary Property
        parameter['maltego'] = param_value.name  # Maltego Property
        parameter['is_value'] = param_value.is_value  # Main Property

        entity['parameters'].append(parameter)

    entity['parameters'] = sorted(entity['parameters'], key=lambda k: k['canari'])
    entities.append(entity)

entities = sorted(entities, key=lambda k: k['class'])


###########################
# WRITE JSON FILE
###########################

with open(filename + ".json", 'w') as fp:
    data = json.dumps(entities, sort_keys=True, indent=4)
    fp.write(data)




###########################
# GENERATE .RST FILE
###########################

template_header = '''
Maltego Entities
===============================================================

.. moduleauthor:: xxx xxx <xxx@xxx.com>
.. sectionauthor:: xxx xxx <xxx@xxx.com>

.. versionadded:: 3.0

'''

template_entity_title = '''\n\n-------------\n\n\n\n\n%s'''

template_entity_data = '''

* Class: ``%s``
* Inherits from: ``%s``
* Class alias: ``%s``
'''

template_entity_table_header = '''
**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property
'''

template_entity_table_data = '''\n    %s,%s,``%s``,``%s``,%s'''


rst_content = template_header
for entity in entities:

    entity_class = entity['class'] if 'class' in entity else '-'
    entity_superclass = entity['superclass'] if 'superclass' in entity else '-'
    entity_aliasclass = entity['alias'] if 'alias' in entity else '-'

    rst_content += template_entity_title % entity_class + "\n" + "-" * len(entity_class) 

    rst_content += template_entity_data % (entity_class, entity_superclass, entity_aliasclass)

    if entity['parameters']:
        rst_content += template_entity_table_header

        for parameter in entity['parameters']:
            p_dname = parameter['display_name'] if 'display_name' in parameter else '-'
            p_type = parameter['type'] if 'type' in parameter else '-'
            p_canari = parameter['canari'] if 'canari' in parameter else '-'
            p_maltego = parameter['maltego'] if 'maltego' in parameter else '-'
            p_isvalue = "Yes" if parameter['is_value'] else "No"

            rst_content += template_entity_table_data % (p_dname, p_type, p_canari, p_maltego, p_isvalue)


###########################
# WRITE .RST FILE
###########################

with open(filename + ".rst", 'w') as fp:
    fp.write(rst_content)



print "Check the files '%s' and '%s'" % (filename + ".rst", filename + ".json")






