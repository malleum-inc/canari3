#!/usr/bin/env python
import sys

from mrbob.rendering import jinja2_env
from mrbob.configurator import Configurator

from canari.maltego.message import StringEntityField, IntegerEntityField, FloatEntityField, Entity, \
    BooleanEntityField, TimeSpanEntityField, DateTimeEntityField, DateEntityField, LongEntityField
from canari.pkgutils.transform import TransformDistribution
from canari.project import CanariProject
from common import canari_main
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
    project = CanariProject(args.out_path)
    args.out_path = project.root_dir
    sys.path.insert(0, project.src_dir)
    return args


@SubCommand(
    canari_main,
    help='Create entities documentation from Canari python classes file.',
    description='Create entities documentation from Canari python classes file.'
)
@Argument(
    '--out-path',
    '-o',
    metavar='<path>',
    help='Where the output entities.rst file will be written to.',
    required=False
)
@Argument(
    'package',
    metavar='<package>',
    help='the name of the canari transforms package to install.'
)
def generate_entities_doc(args):
    args = parse_args(args)

    transform_package = TransformDistribution(args.package)

    jinja2_env.filters['entity_properties'] = \
        lambda v: reversed([(p, getattr(v, p)) for p in dir(v) if isinstance(getattr(v, p), StringEntityField) and
                            not hasattr(Entity, p)])

    def get_property_type(v):
        if isinstance(v, IntegerEntityField):
            return 'int'
        elif isinstance(v, FloatEntityField):
            return 'float'
        elif isinstance(v, BooleanEntityField):
            return 'bool'
        elif isinstance(v, TimeSpanEntityField):
            return 'timedelta'
        elif isinstance(v, DateTimeEntityField):
            return 'datetime'
        elif isinstance(v, DateEntityField):
            return 'date'
        elif isinstance(v, LongEntityField):
            return 'long'
        else:
            return 'str'

    jinja2_env.filters['get_property_type'] = get_property_type

    entity_module = 'canari.maltego.entities' if transform_package.name == 'canari' \
        else '%s.transforms.common.entities' % transform_package.name

    variables = {
        'transform.module': entity_module,
        'transform.entities': transform_package.entities,
        'transform.author': '%s <%s>' % (transform_package.author, transform_package.author_email)
    }

    configurator = Configurator(
            'canari.resources.templates:generate_entities_doc',
            args.out_path,
            {'non_interactive': True},
            variables=variables
    )

    configurator.ask_questions()

    print('Creating entities.rst documentation for %r...' % args.package)
    configurator.render()

    print('done!')
