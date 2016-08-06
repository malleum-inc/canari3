#!/usr/bin/env python
import grp
import os
import sys
import pwd
from stat import ST_MODE, S_ISDIR

from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator, Question

from common import canari_main
from canari.question import parse_bool
from framework import SubCommand, Argument

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.2'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def check_port(configurator, question, answer):
    try:
        if 1 < int(answer) <= 65535:
            return answer
        raise ValueError("Port number needs to be between 1 and 65535.")
    except ValueError, e:
        raise ValidationError(e)


def check_gid(configurator, question, answer):
    try:
        return grp.getgrnam(answer).gr_gid
    except KeyError, e:
        raise ValidationError(e)


def check_uid(configurator, question, answer):
    try:
        return pwd.getpwnam(answer).pw_uid
    except KeyError, e:
        raise ValidationError(e)


def validate_path(configurator, question, answer):
    if not os.path.lexists(answer):
        raise ValidationError("Could not find file %r" % answer)
    return os.path.realpath(answer)


def check_mkdir(configurator, question, answer):
    try:
        if not os.path.lexists(answer):
            os.makedirs(answer)
        elif not S_ISDIR(os.stat(answer)[ST_MODE]):
            raise ValidationError("Invalid path (%s): path must point to a directory not a file." % answer)
        return os.path.realpath(answer)
    except OSError, e:
        raise ValidationError(e)


def check_init_script(configurator, question, answer):
    try:
        if not os.path.lexists(answer):
            os.makedirs(answer)
        elif not S_ISDIR(os.stat(answer)[ST_MODE]):
            raise ValidationError("Invalid path (%s): path must point to a directory not a file." % answer)

        with file(os.path.join(answer, 'plume'), 'w'):
            answer = os.path.realpath(answer)
            configurator.target_directory = answer
            return answer
    except OSError, e:
        raise ValidationError(e)
    except IOError, e:
        raise ValidationError(e)


def configure_ssl(configurator, question, answer):
    answer = answer.lower()
    if answer not in ('0', '1', 'y', 'n'):
        raise ValidationError("Value must be either y/n.")
    answer = int(answer in ('1', 'y'))
    if answer:
        configurator.questions.extend([
            Question(
                    'plume.certificate',
                    'Please specify the path to the public key',
                    default='/etc/ssl/private/server.pem',
                    required=True,
                    post_ask_question='canari.commands.install_plume:validate_path'
            ),
            Question(
                    'plume.private_key',
                    'Please specify the path to the private key',
                    default='/etc/ssl/private/server.pem',
                    required=True,
                    post_ask_question='canari.commands.install_plume:validate_path'
            ),
        ])
    else:
        configurator.variables['plume.certificate'] = ''
        configurator.variables['plume.private_key'] = ''
    return answer


@SubCommand(
    canari_main,
    help='Sets up Canari Plume directory structure and configuration files.',
    description='Sets up Canari Plume directory structure and configuration files.'
)
@Argument(
    '--accept-defaults',
    '-y',
    help='Install Plume with all the defaults in non-interactive mode.',
    default=False,
    action='store_true'
)
def install_plume(opts):

    if not opts.accept_defaults:
        return install_wizard(opts)
    install_defaults(opts)


def install_defaults(opts):
    configurator = Configurator('canari.resources.templates:install_plume', '.',
                                {'non_interactive': True, 'remember_answers': False})

    configurator.variables['plume.venv'] = os.environ.get('VIRTUAL_ENV')
    if configurator.variables['plume.venv']:
        print 'Will use the virtual environment in %r to run Plume...' % configurator.variables['plume.venv']
    configurator.variables['plume.enable_ssl'] = 'n'
    print 'Installing init script to /etc/init.d...'
    configurator.variables['plume.init'] = check_init_script(configurator, '', '/etc/init.d')
    print 'Creating Plume root directory at /var/plume...'
    configurator.variables['plume.dir'] = check_mkdir(configurator, '', '/var/plume')
    print 'The PID file will be at /var/run/plume.pid...'
    configurator.variables['plume.run_dir'] = '/var/run'
    print 'The log files will be at /var/log/plume.log...'
    configurator.variables['plume.log_dir'] = '/var/log'
    configurator.variables['plume.user'] = check_uid(configurator, '', 'nobody')
    configurator.variables['plume.group'] = check_gid(configurator, '', 'nobody')
    print 'The Plume server will under UID/GID=%s/%s...' % (
        configurator.variables['plume.user'], configurator.variables['plume.group'])
    print 'TLS will be disabled by default...'
    configurator.variables['plume.certificate'] = ''
    configurator.variables['plume.private_key'] = ''

    configurator.ask_questions()
    configurator.render()
    finish(configurator)


def install_wizard(opts):
    configurator = Configurator('canari.resources.templates:install_plume', '.',
                                {'non_interactive': False, 'remember_answers': False})
    configurator.ask_questions()

    if os.environ.get('VIRTUAL_ENV'):
        run_venv = parse_bool(
            "--> Canari has detected that you're running this install script from within a virtualenv.\n"
            "--> Would you like to run Plume from this virtualenv (%r) as well?" % os.environ['VIRTUAL_ENV'], True)
        configurator.variables['plume.venv'] = os.environ['VIRTUAL_ENV'] if run_venv else False

    configurator.render()
    finish(configurator)


def finish(configurator):
    print 'Writing canari.conf to %r...' % configurator.variables['plume.dir']

    # move the canari.conf file from the init.d directory to the plume content directory
    src_file = os.path.join(configurator.variables['plume.init'], 'canari.conf')
    dst_file = os.path.join(configurator.variables['plume.dir'], 'canari.conf')

    if src_file != dst_file:
        with file(src_file) as src:
            with file(dst_file, 'w') as dst:
                dst.write(src.read())
        os.unlink(src_file)

    os.chmod(os.path.join(configurator.variables['plume.init'], 'plume'), 0755)

    print 'done!'
