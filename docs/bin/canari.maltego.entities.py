import sys
import re
import json

if len(sys.argv) != 2:
    print "\n\tMaltego Entities Reference Generator\n\n\tUsage:\n\t\t$ python %s <entities.py>\n" % sys.argv[0]
    exit(-1)

filename = sys.argv[0].split('.py')[0]


regex_blocks = 'class .*?\n\n'
regex_class = 'class ([^\(]+)\(([^\)]+)\)'
regex_class_alias = "_alias_ = '([^']+)'"
regex_parameters = "([^\ ]+)[\ ]+=\ ([A-Z][a-z]+[A-Za-z]+)\('([^']+)'([^\)]+)"
regex_parameter_alias = "alias='([^']+)'"
regex_parameter_dname = "display_name='([^']+)'"
regex_parameter_is_value = "is_value=([a-zA-Z]+)"

entities = list()


# Read file
with open(sys.argv[1]) as fp:
    text = fp.read()


# Split in blocks of entities
blocks = re.findall(regex_blocks, text, re.DOTALL)


# Iterate through blocks
for block in blocks:

    params_lines = list()
    entity = dict()
    entity['parameters'] = list()

    for line in block.split('\n'):
        line = line.strip()

        # Ignore empty or irrelevant lines
        if line == "" or line == "pass":
            continue

        # Detect _alias_ / _namespace_
        if line.startswith("_") or line.startswith("class "):
            params_lines.append(line)
            continue

        # Find splitted lines and merge
        if not re.search("[^\ ]+ = [A-Za-z]+\(", line):
            params_lines[-1] += " " + line
            continue

        params_lines.append(line)


    for line in params_lines:

        # Get entity class and entity superclass
        match = re.search(regex_class, line)
        if match:
            entity['class'] = match.group(1)
            entity['superclass'] = match.group(2)
            continue

        # Get class alias
        match = re.search(regex_class_alias, line)
        if match:
            entity['alias'] = match.group(1)

        # Get parameters details
        match = re.search(regex_parameters, line)
        if match:
            parameter = dict()
            parameter['canari'] = match.group(1)
            parameter['type'] = match.group(2)
            parameter['maltego'] = match.group(3)

            submatch = re.search(regex_parameter_alias, match.group(4))
            if submatch:
                parameter['alias'] = submatch.group(1)
                
            submatch = re.search(regex_parameter_dname, match.group(4))
            if submatch:
                parameter['display_name'] = submatch.group(1)

            submatch = re.search(regex_parameter_is_value, match.group(4))
            if submatch:
                parameter['is_value'] = submatch.group(1)
            
            entity['parameters'].append(parameter)
            continue

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
            p_isvalue = "Yes" if 'is_value' in parameter else "No"

            rst_content += template_entity_table_data % (p_dname, p_type, p_canari, p_maltego, p_isvalue)


###########################
# WRITE .RST FILE
###########################

with open(filename + ".rst", 'w') as fp:
    fp.write(rst_content)



print "Check the files '%s' and '%s'" % (filename + ".rst", filename + ".json")


