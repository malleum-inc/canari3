from canari.resource import external_resource
from canari.utils.stack import calling_package

from subprocess import PIPE, Popen
import os
import re


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'RequireSuperUser',
    'Deprecated',
    'EnableRemoteExecution',
    'EnableDebugWindow',
    'ExternalCommand'
]


def RequireSuperUser(transform):
    """
    Marks the transform as a privileged transform which requires root access to execute. Upon transform execution, a
    sudo login box will appear prompting the user to enter their sudo password in the event that there isn't a pre-
    existing sudo session.

    .. note::
    This is not compatible with Windows. UAC must be turned off for privileged functions to execute.

    :param transform: the transform class that will be marked as privileged.
    :return: the superuser'ed transform class.

    :Example:

    @superuser
    dotransform(*args):
        pass
    """
    transform.superuser = True
    return transform


def Deprecated(transform):
    """
    Marks the transform as deprecated.

    :Example:

    @deprecated
    dotransform(*args):
        pass

    :param transform: the transform class that will be marked as deprecated.
    :return: the deprecated transform class.
    """
    transform.deprecated = True
    return transform


def EnableRemoteExecution(transform):
    """
    Marks the transform as deprecated.

    :Example:

    @remote
    dotransform(*args):
        pass

    :param transform: the transform class that will be marked as deprecated.
    :return: the deprecated transform class.
    """
    transform.remote = True
    return transform


def EnableDebugWindow(transform):
    """
    Marks the transform as deprecated.

    :Example:

    @remote
    dotransform(*args):
        pass

    :param transform: the transform class that will be marked as deprecated.
    :return: the deprecated transform class.
    """
    transform.debug = True
    return transform


class ExternalCommand(object):
    def __init__(self, transform_name, transform_args=None, interpreter=None, is_resource=True):
        if transform_args is None:
            transform_args = []
        self._extra_external_args = []

        if interpreter is not None:
            self._extra_external_args.append(interpreter)
            libpath = external_resource(
                os.path.dirname(transform_name),
                '%s.resources.external' % calling_package()
            )
            if interpreter.startswith('perl') or interpreter.startswith('ruby'):
                self._extra_external_args.extend(['-I', libpath])
            elif interpreter.startswith('java'):
                self._extra_external_args.extend(['-cp', libpath])

        if ' ' in transform_name:
            raise ValueError('Transform name %r cannot have spaces.' % transform_name)
        elif not is_resource:
            self._extra_external_args.append(transform_name)
        else:
            self._extra_external_args.append(
                external_resource(
                    transform_name,
                    '%s.resources.external' % calling_package()
                )
            )

        if isinstance(transform_args, basestring):
            self._extra_external_args = re.split(r'\s+', transform_args)
        else:
            self._extra_external_args.extend(transform_args)

    def __call__(self, request, request_xml):
        args = [request.value]
        if isinstance(request.params, list) and request.params:
            args.extend(request.params)
        if request.fields:
            args.append('#'.join(['%s=%s' % (k, v) for k, v in request.fields.iteritems()]))
        if isinstance(request_xml, basestring):
            p = Popen(self._extra_external_args + list(args), stdin=PIPE, stdout=PIPE)
            out, err = p.communicate(request_xml)
            return out
        p = Popen(self._extra_external_args + list(args))
        p.communicate()
        exit(p.returncode)
