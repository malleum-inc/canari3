import inspect
import signal
import sys

import click

from canari.maltego.message import MaltegoMessage, MaltegoTransformExceptionMessage, MaltegoException, Field

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'

__all__ = [
    'on_terminate',
    'message',
    'croak',
    'to_entity',
    'get_transform_version',
    'debug',
    'progress'
]


def on_terminate(func):
    """Register a signal handler to execute when Maltego forcibly terminates the transform."""
    def exit_function(*args):
        func()
        exit(0)
    signal.signal(signal.SIGTERM, exit_function)


def message(m, fd=sys.stdout):
    """Write a MaltegoMessage to stdout and exit successfully"""

    if sys.platform == 'win32':
        decoding = sys.stdout.encoding if sys.version_info[0] > 2 else 'cp1252'
        click.echo(MaltegoMessage(message=m).render(fragment=True, encoding='utf-8').decode(decoding), file=fd)
    else:
        click.echo(MaltegoMessage(message=m).render(encoding='utf-8', fragment=True), file=fd)
    exit(0)


def croak(error, message_writer=message):
    """Throw an exception in the Maltego GUI containing error_msg."""
    if isinstance(error, MaltegoException):
        message_writer(MaltegoTransformExceptionMessage(exceptions=[error]))
    else:
        message_writer(MaltegoTransformExceptionMessage(exceptions=[MaltegoException(error)]))


def to_entity(entity_type, value, fields):
    """
    Internal API: Returns an instance of an entity of type entity_type with the specified value and fields (stored in
    dict). This is only used by the local transform runner as a helper function.
    """
    e = entity_type(value)
    for k, v in fields.items():
        e.fields[k] = Field(k, v)
    return e


def get_transform_version(transform):
    """
    Internal API: Returns the version of the transform function based on the transform function's signature. Currently,
    only two versions are supported (2 and 3). This is what version 2 transform functions look like:

    def transform(request, response):
        ...

    Version 3 transforms have the additional config variable like so:

    def transform(request, response, config):
        ...

    Or can have a varargs parameter as a third argument:

    def transform(request, response, *args):
        ...

    In both cases, version 3 transforms will be passed a local copy of the canari configuration object as the third
    argument. However, in the latter example, the configuration object will be stored in a tuple (i.e. (config,)).
    """

    if sys.version_info[0] > 3:
        spec = inspect.getfullargspec(transform)
    else:
        spec = inspect.getargspec(transform)

    if spec.varargs:
        return 3

    n = len(spec.args)

    if 2 <= n <= 3:
        return n

    raise Exception('Could not determine transform version.')


def debug(*args):
    """Send debug messages to the Maltego console."""
    for i in args:
        click.echo('D:%s' % str(i), err=True)


def progress(i):
    """Send a progress report to the Maltego console."""
    click.echo('%%%d' % min(max(i, 0), 100), err=True)
