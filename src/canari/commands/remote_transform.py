import argparse

from canari.commands.common import canari_main
from canari.commands.framework import SubCommand, Argument
from canari.maltego.message import _Entity, Field, Limits, MaltegoMessage
from canari.maltego.runner import remote_canari_transform_runner, console_writer
from canari.mode import set_canari_mode, CanariMode

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2016, Canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = []


def split_validate(value, type_):
    if '=' not in value:
        print 'Invalid %s ("%s") specified. Must be in "name=value" format.' % (type_, value)
        exit(-1)
    return value.split('=', 1)


@SubCommand(
    canari_main,
    help='Runs Canari local transforms in a terminal-friendly fashion.',
    description='Runs Canari local transforms in a terminal-friendly fashion.'
)
@Argument(
    'host',
    metavar='<host[:port]>',
    help='The hostname or IP address and optionally the port of the remote Canari transform server.'
)
@Argument(
    'transform',
    metavar='<transform>',
    help='The UUID of the transform you wish to run (e.g. sploitego3.IPToLocation).'
)
@Argument(
    'input',
    metavar='<entity name>=<value>',
    help='The name and value of the input entity being passed into the local transform (e.g. "maltego.Person=Bob").'
)
@Argument(
    '-f',
    '--entity-field',
    metavar='<name>=<value>',
    # nargs='*',
    help='The entity field name and value pair (e.g. "person.firstname=Bob"). Can be specified multiple times.',
    action='append',
    default=[]
)
@Argument(
    '-p',
    '--transform-parameter',
    metavar='<name>=<value>',
    # nargs='*',
    help='Transform parameter name and value pair (e.g. "api.key=123"). Can be specified multiple times.',
    action='append',
    default=[]
)
@Argument(
    '-r',
    '--raw-output',
    help='Print out raw XML output instead of prettified format.',
    action='store_true',
    default=False
)
@Argument(
    '--ssl',
    help='Perform request over HTTPS (default: False).',
    action='store_true',
    default=False
)
@Argument(
    '-b',
    '--base-path',
    metavar='<base path>',
    default='/',
    help='The base path of the Canari transform server (default: "/").'
)
@Argument(
    '--soft-limit',
    type=int,
    default=500,
    metavar='<soft limit>',
    help='Set the soft limit (default: 500)'
)
@Argument(
    '--hard-limit',
    type=int,
    metavar='<hard limit>',
    default=10000,
    help='Set the hard limit (default: 10000)'
)
@Argument(
    '-v',
    '--verbose',
    help='Enable verbose debug mode.',
    action='store_true',
    default=False
)
def remote_transform(args):
    if args.verbose:
        set_canari_mode(CanariMode.LocalDebug)

    entity_type, entity_value = split_validate(args.input, 'entity')
    fields = {}
    params = []

    for f in args.entity_field:
        name, value = split_validate(f, 'entity field')
        fields[name] = Field(name=name, value=value)

    for p in args.transform_parameter:
        name, value = split_validate(p, 'transform parameter')
        params.append(Field(name=name, value=value))

    try:
        r = remote_canari_transform_runner(
            args.host,
            args.base_path,
            args.transform,
            [_Entity(type=entity_type, value=entity_value, fields=fields)],
            params,
            Limits(soft=args.soft_limit, hard=args.hard_limit),
            args.ssl
        )

        if r.status == 200:
            data = r.read()
            if args.raw_output:
                print data
                exit(0)
            else:
                console_writer(MaltegoMessage.parse(data))
                exit(0)

        print 'ERROR: Received status %d for %s://%s/%s. Are you sure you got the right server?' % (
            r.status,
            'https' if args.ssl else 'http',
            args.host,
            args.transform
        )
    except Exception, e:
        print 'ERROR: %s' % e
    exit(-1)
