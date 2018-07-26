import sys

from six import string_types

from canari.utils.common import find_pysudo

if sys.version_info[0] > 2:
    from http.client import HTTPSConnection, HTTPConnection
else:
    # noinspection PyUnresolvedReferences
    from httplib import HTTPSConnection, HTTPConnection

import subprocess
import os
import sys
import traceback
from collections import defaultdict
from canari.mode import is_debug_exec_mode
from importlib import import_module

import re
from xml.etree.cElementTree import fromstring

from safedexml import Model

from canari.config import load_config
from canari.maltego.message import MaltegoTransformResponseMessage, UIMessage, MaltegoTransformRequestMessage, Field, \
    MaltegoException, EntityTypeFactory, Entity, MaltegoMessage, Limits
from canari.maltego.utils import message, on_terminate, to_entity, croak, highlight

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'

__all__ = [
    'sudo',
    'local_transform_runner',
    'remote_canari_transform_runner',
    'scriptable_transform_runner',

]


def sudo(args):
    environ = os.environ.copy()
    environ['SUDO_ASKPASS'] = find_pysudo()
    p = subprocess.Popen(['sudo', '-A'] + args, env=environ)
    p.communicate()
    return p.returncode


def load_object(classpath):
    package, cls = re.search(r'^(.*)\.([^.]+)$', classpath).groups()
    module = import_module(package)
    return module.__dict__[cls]


def remote_canari_transform_runner(host, base_path, transform, entities, parameters, limits, is_ssl=False):
    c = HTTPSConnection(host) if is_ssl else HTTPConnection(host)

    m = MaltegoTransformRequestMessage()

    for e in entities:
        m += e

    for p in parameters:
        m += p

    m += limits

    message = MaltegoMessage(message=m).render()
    path = re.sub(r'/+', '/', '/'.join([base_path, transform]))

    if is_debug_exec_mode():
        sys.stderr.write("Sending following message to {}{}:\n{}\n\n".format(host, path, message))

    c.request('POST', path, message, headers={'Content-Type': 'application/xml'})

    return c.getresponse()


def local_transform_runner(transform_py_name, value, fields, params, config, message_writer=message):
    """
    Internal API: The local transform runner is responsible for executing the local transform.

    Parameters:

    transform      - The name or module of the transform to execute (i.e sploitego.transforms.whatismyip).
    value          - The input entity value.
    fields         - A dict of the field names and their respective values.
    params         - The extra parameters passed into the transform via the command line.
    config         - The Canari configuration object.
    message_writer - The message writing function used to write the MaltegoTransformResponseMessage to stdout. This is
                     can either be the console_message or message functions. Alternatively, the message_writer function
                     can be any callable object that accepts the MaltegoTransformResponseMessage as the first parameter
                     and writes the output to a destination of your choosing.

    This helper function is only used by the run-transform, debug-transform, and dispatcher commands.
    """

    try:
        transform = load_object(transform_py_name)()

        if os.name == 'posix' and transform.superuser and os.geteuid():
            rc = sudo(sys.argv)
            if rc == 1:
                message_writer(MaltegoTransformResponseMessage() + UIMessage('User cancelled transform.'))
            elif rc == 2:
                message_writer(MaltegoTransformResponseMessage() + UIMessage('Too many incorrect password attempts.'))
            elif rc:
                message_writer(MaltegoTransformResponseMessage() + UIMessage('Unknown error occurred.'))
            exit(rc)

        on_terminate(transform.on_terminate)

        request = MaltegoTransformRequestMessage(
            parameters={'canari.local.arguments': Field(name='canari.local.arguments', value=params)}
        )

        request._entities = [to_entity(transform.input_type, value, fields)]
        request.limits = Limits(soft=10000)

        msg = transform.do_transform(
            request,
            MaltegoTransformResponseMessage(),
            config
        )
        if isinstance(msg, MaltegoTransformResponseMessage):
            message_writer(msg)
        elif isinstance(msg, string_types):
            raise MaltegoException(msg)
        else:
            raise MaltegoException('Could not resolve message type returned by transform.')
    except MaltegoException as me:
        croak(me, message_writer)
    except KeyboardInterrupt:
        # Ensure that the keyboard interrupt handler does not execute twice if a transform is sudo'd
        if (transform.superuser and not os.geteuid()) or (not transform.superuser and os.geteuid()):
            transform.on_terminate()
    except Exception:
        croak(traceback.format_exc(), message_writer)


class Response(object):
    def __init__(self, maltego_response):
        self._response = maltego_response
        self._entities = [EntityTypeFactory.create(e.type)(e) for e in maltego_response.entities]
        self._messages = defaultdict(list)
        for m in maltego_response.messages:
            self._messages[m.type].append(m.message)

    def toXML(self):
        return self._response.render(fragment=True)

    @property
    def entities(self):
        return self._entities

    @property
    def messages(self):
        return self._messages


scriptable_api_initialized = False


def scriptable_transform_runner(transform, value, fields, params, config):
    global scriptable_api_initialized
    if not scriptable_api_initialized:
        scriptable_api_initialized = True

        def run_transform(self, transform, params=None, config=None):
            if isinstance(transform, string_types):
                transform = load_object(transform)
            return scriptable_transform_runner(
                transform,
                self.value,
                self.fields,
                params or [],
                config or load_config()
            )

        Entity.run_transform = run_transform

    request = MaltegoTransformRequestMessage(
        parameters={'canari.local.arguments': Field(name='canari.local.arguments', value=params)}
    )

    request._entities = [to_entity(transform.input_type, value, fields)]
    request.limits = Limits(soft=10000)

    msg = transform().do_transform(
        request,
        MaltegoTransformResponseMessage(),
        config
    )
    if isinstance(msg, MaltegoTransformResponseMessage):
        return Response(msg)
    elif isinstance(msg, string_types):
        raise MaltegoException(msg)
    else:
        raise MaltegoException('Could not resolve message type returned by transform.')


def console_writer(msg, tab=-1):
    """
    Internal API: Returns a prettified tree-based output of an XML message for debugging purposes. This helper function
    is used by the debug-transform command.
    """
    tab += 1

    if isinstance(msg, Model):
        msg = fromstring(msg.render())

    print('%s`- %s: %s %s' % (
        '  ' * tab,
        highlight(msg.tag, None, True),
        highlight(msg.text, 'red', False) if msg.text is not None else '',
        highlight(msg.attrib, 'green', True) if msg.attrib.keys() else ''
    ))
    for c in msg.getchildren():
        print('  %s`- %s: %s %s' % (
            '  ' * tab,
            highlight(c.tag, None, True),
            highlight(c.text, 'red', False) if c.text is not None else '',
            highlight(c.attrib, 'green', True) if c.attrib.keys() else ''
        ))
        for sc in c.getchildren():
            tab += 1
            console_writer(sc, tab)
            tab -= 1
