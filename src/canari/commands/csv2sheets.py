#!/usr/bin/env python
from collections import OrderedDict

from framework import Argument, SubCommand
from common import canari_main

from csv import reader, DictWriter


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.4'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


@SubCommand(
    canari_main,
    help='Convert mixed entity type CSVs to separated CSV sheets.',
    description='Convert mixed entity type CSVs to separated CSV sheets.'
)
@Argument(
    'graph',
    metavar='<graph csv>',
    help='The CSV file containing the output from the mtgx2csv command.'
)
@Argument(
    'prefix',
    metavar='[sheet prefix]',
    nargs='?',
    help='The prefix to prepend to the generated CSV files.'
)
def csv2sheets(opts):

    if not opts.graph.endswith('.csv'):
        print "Invalid file type: %s. Please make sure you run this command against a CSV " \
              "file generated from 'canari mtgx2csv'." % opts.graph
        exit(-1)
    opts.prefix = opts.prefix or opts.graph.split('.', 1)[0]

    sheets = {}
    sheet_headers = {}

    try:
        with file(opts.graph) as csvfile:
            for row in reader(csvfile):
                fv = OrderedDict(column.split('=', 1) for column in row)
                entity_type = fv.pop('Entity Type')
                headers = fv.keys()
                if entity_type not in sheets:
                    sheets[entity_type] = [fv]
                    sheet_headers[entity_type] = headers
                    continue
                else:
                    sheets[entity_type].append(fv)
                if len(headers) > len(sheet_headers[entity_type]):
                    sheet_headers[entity_type].extend([h for h in headers if h not in sheet_headers[entity_type]])

        for entity_type in sheets:
            filename = '%s_%s.csv' % (opts.prefix, entity_type)
            print 'Writing %s sheet to %s...' % (entity_type, filename)
            with open(filename, 'wb') as csvfile:
                csv = DictWriter(csvfile, sheet_headers[entity_type])
                csv.writeheader()
                csv.writerows(sheets[entity_type])
    except IOError, e:
        print 'csv2sheets: %s' % e
        exit(-1)