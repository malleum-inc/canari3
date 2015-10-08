#!/usr/bin/env python
import hashlib
import os
import sys
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from ssl import wrap_socket, CERT_NONE
from socket import getfqdn
from urlparse import urlsplit
import re

from canari.maltego.utils import get_transform_version
from canari.maltego.message import (MaltegoTransformResponseMessage, MaltegoException, MaltegoTransformRequestMessage,
                                    MaltegoTransformExceptionMessage, MaltegoMessage)
from canari.mode import set_canari_mode, CanariMode
from canari.pkgutils.transform import TransformDistribution
from common import fix_binpath, canari_main
from framework import SubCommand, Argument
from canari.config import config
import canari.resource


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.8'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def message(m, response):
    """Write a MaltegoMessage to stdout and exit successfully"""

    response.send_response(200)
    response.send_header('Content-Type', 'text/xml')
    response.send_header('Connection', 'close')
    response.end_headers()

    v = None
    if isinstance(m, basestring):
        for url in re.findall("<iconurl>\s*(file://[^\s<]+)\s*</iconurl>(?im)", m):
            path = '/%s' % hashlib.md5(url).hexdigest()
            new_url = '%s://%s%s' % ('https' if response.server.is_ssl else 'http', response.server.hostname, path)
            if path not in response.server.resources:
                response.server.resources[path] = url[7:]
            m.replace(url, new_url, 1)
        v = m
    else:
        v = MaltegoMessage(m).render(fragment=True)
        # Get rid of those nasty unicode 32 characters
    response.wfile.write(v)


def croak(error_msg, response):
    """Throw an exception in the Maltego GUI containing error_msg."""

    response.send_response(200)
    response.send_header('Content-Type', 'text/xml')
    response.send_header('Connection', 'close')
    response.end_headers()

    response.wfile.write(
        MaltegoMessage(
            message=MaltegoTransformExceptionMessage(exceptions=[MaltegoException(error_msg)])
        ).render(fragment=True)
    )


class MaltegoTransformRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    server_version = 'Canari/1.0'
    count = 0

    def dotransform(self, transform, valid_input_entity_types):
        try:
            if 'Content-Length' not in self.headers:
                self.send_error(500, 'What?')
                return
            request_str = self.rfile.read(int(self.headers['Content-Length']))

            msg = MaltegoTransformRequestMessage.parse(request_str).message

            e = msg.entity
            entity_type = e.type

            if valid_input_entity_types and entity_type not in valid_input_entity_types:
                self.send_error(400, 'Unsupported input entity!')
                return

            for k, i in msg.parameters.iteritems():
                if '.' in k:
                    config[k.replace('.', '/', 1)] = i
                else:
                    config['plume/%s' % k] = i

            msg = transform(
                msg,
                request_str if hasattr(transform, 'cmd') and
                callable(transform.cmd) else MaltegoTransformResponseMessage()
            ) if get_transform_version(transform) == 2 else transform(
                msg,
                request_str if hasattr(transform, 'cmd') and
                callable(transform.cmd) else MaltegoTransformResponseMessage(),
                config
            )

            if isinstance(msg, MaltegoTransformResponseMessage) or isinstance(msg, basestring):
                message(msg, self)
                return
            else:
                raise MaltegoException('Could not resolve message type returned by transform.')

        except MaltegoException, me:
            croak(str(me), self)
        except Exception, e:
            croak(str(e), self)

    def do_POST(self):
        path = urlsplit(self.path or '/').path
        if path not in self.server.transforms:
            self.send_error(404, "Duh?")
        else:
            self.dotransform(*self.server.transforms[path])

    def do_GET(self):
        path = urlsplit(self.path or '/').path
        if path in self.server.transforms:
            self.send_error(200, 'Yes')
            return
        elif path in self.server.resources:
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(file(self.server.resources[path]).read())
            return

        self.send_error(404, 'No')


class MaltegoHTTPServer(HTTPServer):
    server_name = 'Canari'
    resources = {}
    is_ssl = False

    def __init__(self, server_address=('', 8080), RequestHandlerClass=MaltegoTransformRequestHandler,
                 bind_and_activate=True, transforms={}, hostname=getfqdn()):
        HTTPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.transforms = transforms
        self.hostname = hostname


class SecureMaltegoHTTPServer(MaltegoHTTPServer):
    is_ssl = True

    def __init__(self, server_address=('', 8080), RequestHandlerClass=MaltegoTransformRequestHandler,
                 bind_and_activate=True, transforms={}, cert='cert.pem', hostname=getfqdn()):
        MaltegoHTTPServer.__init__(
            self,
            server_address,
            RequestHandlerClass,
            bind_and_activate=bind_and_activate,
            transforms=transforms,
            hostname=hostname
        )
        self.socket = wrap_socket(self.socket, server_side=True, certfile=cert, cert_reqs=CERT_NONE)


class AsyncSecureMaltegoHTTPServer(ThreadingMixIn, SecureMaltegoHTTPServer):
    pass


class AsyncMaltegoHTTPServer(ThreadingMixIn, MaltegoHTTPServer):
    pass


def parse_args(args):
    if not args.hostname:
        args.hostname = getfqdn()
    return args


def monkey_patch(server):
    imgres = canari.resource.image_resource
    canari.resource.image_resource = lambda name, pkg=None: '%s://%s/%s' % (
        'https' if server.is_ssl else 'http',
        server.hostname,
        imgres(hashlib.md5(name).hexdigest())
    )
    canari.resource.icon_resource = canari.resource.image_resource
    callpkg = canari.resource.calling_package
    canari.resource.calling_package = lambda frame=4: callpkg(frame)


@SubCommand(
    canari_main,
    help='Runs a transform server for the given packages.',
    description='Runs a transform server for the given packages.'
)
@Argument(
    'packages',
    metavar='<package>',
    help='The name of the transform packages you wish to host (e.g. mypkg.transforms).',
    nargs='+'
)
@Argument(
    '--port',
    metavar='<port>',
    default=-1,
    type=int,
    help='The port the server will run on.'
)
@Argument(
    '--disable-ssl',
    action='store_true',
    default=False,
    help='Any extra parameters that can be sent to the local transform.'
)
@Argument(
    '--enable-privileged',
    action='store_true',
    default=False,
    help='DANGEROUS: permit TDS to run packages that require elevated privileges.'
)
@Argument(
    '--listen-on',
    metavar='[address]',
    default='',
    help='The address of the interface to listen on.'
)
@Argument(
    '--cert',
    metavar='[certificate]',
    default='cert.pem',
    help='The name of the certificate file used for the server in PEM format.'
)
@Argument(
    '--hostname',
    metavar='[hostname]',
    default=None,
    help='The hostname of this transform server.'
)
@Argument(
    '--daemon',
    default=False,
    action='store_true',
    help='Daemonize server (fork to background).'
)
def run_server(args):

    set_canari_mode(CanariMode.RemoteRunnerDispatch)
    fix_binpath(config['default/path'])
    opts = parse_args(args)

    if opts.port == -1:
        opts.port = 443 if not opts.disable_ssl else 80

    if os.name == 'posix' and os.geteuid() and (opts.port <= 1024 or opts.enable_privileged):
        print ('You must run this server as root to continue...')
        os.execvp('sudo', ['sudo'] + sys.argv)

    transforms = {}

    print ('Loading transform packages...')

    try:
        for pkg_name in opts.packages:

            t = TransformDistribution(pkg_name)

            print ('Loading transform package %s' % pkg_name)
            for transform_module in t.remote_transforms:
                transform_name = transform_module.__name__

                if os.name == 'posix' and hasattr(transform_module.dotransform, 'privileged') and \
                        (os.geteuid() or not opts.enable_privileged):
                    continue

                if hasattr(transform_module.dotransform, 'remote') and transform_module.dotransform.remote:
                    print ('Loading %s at /%s...' % (transform_name, transform_name))
                    inputs = []
                    if hasattr(transform_module.dotransform, 'inputs'):
                        for category, entity_type in transform_module.dotransform.inputs:
                            inputs.append(entity_type._type_)
                            inputs.append(entity_type._v2type_)
                    transforms['/%s' % transform_name] = (transform_module.dotransform, inputs)

    except Exception, e:
        print (str(e))
        print ('Failed to load transforms... exiting')
        exit(-1)

    if not transforms:
        print ("Couldn't find any remote transforms... you sure you got this right?")
        exit(-1)

    httpd = None

    print ('Starting web server on %s:%s...' % (opts.listen_on, opts.port))
    server_address = (opts.listen_on, opts.port)

    if not opts.disable_ssl:
        if not os.path.exists(opts.cert):
            print ('The certificate file %r does not exist. Please create a PEM file...' % opts.cert)
            exit(-1)
        print ('Making it secure (1337)...')
        httpd = AsyncSecureMaltegoHTTPServer(server_address=server_address,
                                             transforms=transforms, cert=opts.cert, hostname=opts.hostname)
    else:
        print ('Really? Over regular HTTP? What a shame...')
        httpd = AsyncMaltegoHTTPServer(server_address=server_address, transforms=transforms, hostname=opts.hostname)

    monkey_patch(httpd)

    if not opts.daemon or not os.fork():
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
    exit(0)
