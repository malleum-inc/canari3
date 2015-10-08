#!/usr/bin/env python

from csv import writer
import os
from xml.etree.cElementTree import XML
from zipfile import ZipFile

from framework import SubCommand, Argument
from common import canari_main, to_utf8


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.5'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


@SubCommand(
    canari_main,
    help='Convert Maltego graph files (*.mtgx) to comma-separated values (CSV) file.',
    description='Convert Maltego graph files (*.mtgx) to comma-separated values (CSV) file.'
)
@Argument(
    'graph',
    metavar='<graph>',
    help='The name of the graph file you wish to convert to CSV.',
)
def mtgx2csv(opts):

    zipfile = ZipFile(opts.graph)
    graphs = filter(lambda x: x.endswith('.graphml'), zipfile.namelist())

    for f in graphs:
        filename = '%s_%s' % (opts.graph.replace('.', '_', 1), os.path.basename(f).replace('.graphml', '.csv', 1))
        print 'Writing data from %s/%s to %s...' % (opts.graph, f, filename)
        with open(filename, 'wb') as csvfile:
            csv = writer(csvfile)
            xml = XML(zipfile.open(f).read())
            links = {}
            for edge in xml.findall('{http://graphml.graphdrawing.org/xmlns}graph/'
                                    '{http://graphml.graphdrawing.org/xmlns}edge'):
                src = edge.get('source')
                dst = edge.get('target')
                if src not in links:
                    links[src] = dict(in_=0, out=0)
                if dst not in links:
                    links[dst] = dict(in_=0, out=0)
                links[src]['out'] += 1
                links[dst]['in_'] += 1

            for node in xml.findall('{http://graphml.graphdrawing.org/xmlns}graph/'
                                    '{http://graphml.graphdrawing.org/xmlns}node'):

                node_id = node.get('id')
                node = node.find('{http://graphml.graphdrawing.org/xmlns}data/'
                                 '{http://maltego.paterva.com/xml/mtgx}MaltegoEntity')

                row = [to_utf8(('Entity Type=%s' % node.get('type')).strip())]
                for prop in node.findall('{http://maltego.paterva.com/xml/mtgx}Properties/'
                                         '{http://maltego.paterva.com/xml/mtgx}Property'):
                    value = prop.find('{http://maltego.paterva.com/xml/mtgx}Value').text or ''
                    row.append(to_utf8(('%s=%s' % (prop.get('displayName'), value)).strip()))
                row.append('Incoming Links=%s' % links.get(node_id, {}).get('in_', 0))
                row.append('Outgoing Links=%s' % links.get(node_id, {}).get('out', 0))
                csv.writerow(row)