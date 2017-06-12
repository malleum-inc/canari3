#!/usr/bin/env python

# Builtin imports
import logging
import os
import sys
import tempfile
import traceback
from ConfigParser import NoSectionError
from hashlib import md5
from logging.handlers import RotatingFileHandler

from flask import Flask, Response, request, safe_join

import canari.resource
from canari.commands.common import fix_binpath, fix_pypath
from canari.config import load_config, OPTION_REMOTE_PATH
from canari.maltego.entities import Phrase, Unknown
from canari.maltego.message import (MaltegoMessage, MaltegoTransformResponseMessage, MaltegoTransformExceptionMessage,
                                    MaltegoException)
from canari.maltego.transform import Transform
from canari.mode import set_canari_mode, CanariMode
from canari.pkgutils.transform import TransformDistribution

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.5'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'application'
]

# Initialize Canari modes and bin path
set_canari_mode(CanariMode.RemotePlumeDispatch)
fix_binpath(load_config()[OPTION_REMOTE_PATH])
fix_pypath()


def get_image_path(i):
    return os.path.join('static', md5(i).hexdigest())


def get_image_url(i):
    return '%s/static/%s' % (request.host_url, md5(i).hexdigest())


# Monkey patch our resource lib to automatically rewrite icon urls
_icon_resource = canari.resource.icon_resource
canari.resource.icon_resource = lambda name, pkg=None: get_image_url(_icon_resource(name, pkg))

_calling_package = canari.resource.calling_package
canari.resource.calling_package = lambda frame=4: _calling_package(frame)

# Use temporary directory as Python Egg Cache
os.environ['PYTHON_EGG_CACHE'] = tempfile.gettempdir()


class Version(Transform):
    input_type = Phrase

    def do_transform(self, r, res, config):
        if r.entity.value == 'version':
            res += Phrase('Canari v%s' % __version__)
        return res


class Plume(Flask):
    four_o_four = 'Whaaaaat?'

    def __init__(self, import_name, *args, **kwargs):
        super(Plume, self).__init__(import_name, *args, **kwargs)
        self.transforms = {}
        self.resources = []
        self._initialize()

    def _copy_images(self, pkg):
        if pkg.endswith('.transforms'):
            pkg = pkg.replace('.transforms', '')
        for i in canari.resource.image_resources(pkg):
            img_name = get_image_path(i)
            self.resources.append(img_name)
            if not os.path.exists(img_name):
                print 'Copying %s to %s...' % (i, img_name)
                with open(i, mode='rb') as src:
                    with open(img_name, mode="wb") as dst:
                        dst.write(src.read())

    def _initialize(self):

        packages = None

        # Read packages that are to be loaded at runtime
        try:
            config = load_config()
            packages = config['canari.remote.packages']
        except NoSectionError:
            sys.stderr.write('Exiting... You did not specify a [canari.remote] section and a "packages" '
                             'option in your canari.conf file!\n')
            exit(-1)

        # Is packages not blank
        if not packages:
            sys.stderr.write(
                'Exiting... You did not specify any transform packages to load in your canari.conf file!\n')
            exit(-1)
        elif isinstance(packages, basestring):
            packages = [packages]

        # Create the static directory for static file loading
        if not os.path.exists('static'):
            os.mkdir('static', 0755)

        # Iterate through the list of packages to load
        for p in packages:
            # Copy all the image resource files in case they are used as entity icons

            distribution = TransformDistribution(p)

            sys.stderr.write('Loading transform package %s\n' % repr(p))

            for transform in distribution.remote_transforms:
                transform_name = transform().name
                sys.stderr.write('Loading transform %s at /%s...\n' % (repr(transform_name), transform_name))
                if os.name == 'posix' and transform.superuser and os.geteuid() and __name__.startswith('_mod_wsgi_'):
                    sys.stderr.write('WARNING: mod_wsgi does not allow applications to run with root privileges. '
                                     'Transform %s ignored...\n' % repr(transform_name))
                    continue

                self.transforms[transform_name] = transform

            self._copy_images(p)

        if not self.transforms:
            sys.stderr.write('Exiting... Your transform packages have no remote transforms.\n')
            exit(-1)

        self.transforms['canari.Version'] = Version


# Create our Flask app.
application = Plume(__name__)


def croak(cause):
    """Throw an exception in the Maltego GUI containing cause.

    :param cause: a string containing the issue description.
    """
    return MaltegoMessage(
        message=MaltegoTransformExceptionMessage(
            exceptions=[
                MaltegoException(cause)
            ]
        )
    ).render()


def message(msg):
    """Write a MaltegoMessage to stdout and exit successfully"""
    v = MaltegoMessage(message=msg).render()
    return Response(v, status=200, mimetype='text/xml')


def do_transform(transform):
    try:
        # Let's get an XML object tree
        req = MaltegoMessage.parse(request.data).message

        # If our transform define an input entity type then we should check
        # whether the request contains the right type
        if transform.input_type and transform.input_type is not Unknown and \
                not isinstance(req.entity, transform.input_type):
            return Response(application.four_o_four, status=404)

        # Execute it!
        msg = transform().do_transform(
            req,
            MaltegoTransformResponseMessage(),
            load_config()
        )

        # Let's serialize the return response and clean up whatever mess was left behind
        if isinstance(msg, MaltegoTransformResponseMessage):
            return message(msg)
        else:
            raise MaltegoException(str(msg))

    # Unless we croaked somewhere, then we need to fix things up here...
    except MaltegoException, me:
        return croak(str(me))
    except Exception:
        if application.debug:
            return croak(traceback.format_exc())
        else:
            return croak('Transform execution failed.')


# This is where the TDS will ask: "Are you a transform?" and we say "200 - Yes I am!" or "404 - PFO"
@application.route('/<transform_name>', methods=['GET'])
def transform_checker(transform_name):
    if transform_name in application.transforms:
        return Response('Yes?', status=200)
    return Response(application.four_o_four, status=404)


@application.route('/static/<resource_name>', methods=['GET'])
def static_fetcher(resource_name):
    resource_name = safe_join('static', resource_name)
    if resource_name in application.resources:
        return Response(file(resource_name, mode='rb').read(), status=200, mimetype='application/octet-stream')
    return Response(application.four_o_four, status=404)


# This is where we process a transform request.
@application.route('/<transform_name>', methods=['POST'])
def transform_runner(transform_name):
    if transform_name not in application.transforms:
        return Response(application.four_o_four, status=404)
    return do_transform(application.transforms[transform_name])


# To run Flask standalone just type `python -m canari.tas.plume`
if __name__ == '__main__':
    set_canari_mode(CanariMode.RemotePlumeDebug)
    handler = RotatingFileHandler('plume.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    application.logger.addHandler(handler)
    application.run(debug=True)
