import traceback

import click

from canari.maltego.message import _Entity, Field, Limits, MaltegoMessage
from canari.maltego.runner import remote_canari_transform_runner, console_writer
from canari.mode import set_canari_mode, CanariMode

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2016, Canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'

__all__ = [
    'remote_transform'
]


def split_validate(value, type_):
    if '=' not in value:
        click.echo('Invalid %s ("%s") specified. Must be in "name=value" format.' % (type_, value), err=True)
        exit(-1)
    return value.split('=', 1)


def remote_transform(host, transform, input, entity_field, transform_parameter, raw_output, 
                     ssl, base_path, soft_limit, hard_limit, verbose):
    if verbose:
        set_canari_mode(CanariMode.LocalDebug)

    entity_type, entity_value = split_validate(input, 'entity')
    fields = {}
    params = []

    for f in entity_field:
        name, value = split_validate(f, 'entity field')
        fields[name] = Field(name=name, value=value)

    for p in transform_parameter:
        name, value = split_validate(p, 'transform parameter')
        params.append(Field(name=name, value=value))

    try:
        r = remote_canari_transform_runner(
            host,
            base_path,
            transform,
            [_Entity(type=entity_type, value=entity_value, fields=fields)],
            params,
            Limits(soft=soft_limit, hard=hard_limit),
            ssl
        )

        if r.status == 200:
            data = r.read().decode('utf8')
            if raw_output:
                click.echo(data, err=True)
                exit(0)
            else:
                console_writer(MaltegoMessage.parse(data))
                exit(0)

        click.echo('ERROR: Received status %d for %s://%s/%s. Are you sure you got the right server?' % (
            r.status,
            'https' if ssl else 'http',
            host,
            transform
        ), err=True)
        
        if verbose:
            click.echo(r.read(), err=True)
    except Exception as e:
        click.echo('ERROR: %s' % e, err=True)
        if verbose:
            traceback.print_exc()
    exit(-1)
