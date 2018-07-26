from __future__ import print_function

import inspect
import signal
import sys
import os

from canari.maltego.entities import Unknown
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
    'highlight',
    'croak',
    'guess_entity_type',
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
        print(
            MaltegoMessage(message=m).render(fragment=True, encoding='utf-8').decode(decoding),
            file=fd
        )
    else:
        print(
            MaltegoMessage(message=m).render(fragment=True),
            file=fd
        )
    sys.exit(0)


def highlight(s, color, bold):
    """
    Internal API: Returns the colorized version of the text to be returned to a POSIX terminal. Not compatible with
    Windows (yet).
    """
    if os.name == 'posix':
        attr = []
        if color == 'green':
            # green
            attr.append('32')
        elif color == 'red':
            # red
            attr.append('31')
        else:
            attr.append('30')
        if bold:
            attr.append('1')
        s = '\x1b[%sm%s\x1b[0m' % (';'.join(attr), s)

    return s


def croak(error, message_writer=message):
    """Throw an exception in the Maltego GUI containing error_msg."""
    if isinstance(error, MaltegoException):
        message_writer(MaltegoTransformExceptionMessage(exceptions=[error]))
    else:
        message_writer(MaltegoTransformExceptionMessage(exceptions=[MaltegoException(error)]))


def guess_entity_type(transform_module, fields):
    """
    Internal API: Returns the entity type based on the following best match algorithm:

    1. If a transform does not specify the input entity types, the Unknown entity will be returned.
    2. If a transform only has one input entity type, then that entity type will be returned.
    3. If a transform has more than one input entity type, then the entity type that has the
       most number of matching entity fields in the entity's class definition will be returned.

    This is only used by the local transform runner to detect the input entity type since this information is excluded
    at run-time.
    """
    if not hasattr(transform_module.dotransform, 'inputs') or not transform_module.dotransform.inputs:
        return Unknown
    if len(transform_module.dotransform.inputs) == 1 or not fields:
        return transform_module.dotransform.inputs[0][1]
    num_matches = 0
    best_match = Unknown
    for category, entity_type in transform_module.dotransform.inputs:
        l = len(set(entity_type._fields_to_properties_.keys()).intersection(fields.keys()))
        if l > num_matches:
            num_matches = l
            best_match = entity_type
    return best_match


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
    spec = inspect.getargspec(transform)
    if spec.varargs is not None:
        return 3
    n = len(spec.args)
    if 2 <= n <= 3:
        return n
    raise Exception('Could not determine transform version.')


def debug(*args):
    """Send debug messages to the Maltego console."""
    for i in args:
        print('D:%s' % str(i), file=sys.stderr)


def progress(i):
    """Send a progress report to the Maltego console."""
    print('%%%d' % min(max(i, 0), 100), file=sys.stderr)
