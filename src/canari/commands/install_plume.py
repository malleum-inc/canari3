import os

import click
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator, Question

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.2'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'


def check_port(configurator, question, answer):
    try:
        if 1 < int(answer) <= 65535:
            return answer
        raise ValueError("Port number needs to be between 1 and 65535.")
    except ValueError as e:
        raise ValidationError(e)


def check_gid(configurator, question, answer):
    try:
        import grp
        return grp.getgrnam(answer).gr_gid
    except KeyError as e:
        raise ValidationError(e)


def check_uid(configurator, question, answer):
    try:
        import pwd
        return pwd.getpwnam(answer).pw_uid
    except KeyError as e:
        raise ValidationError(e)


def validate_path(configurator, question, answer):
    if not os.path.lexists(answer):
        raise ValidationError("Could not find file %r" % answer)
    return os.path.realpath(answer)


def check_mkdir(configurator, question, answer):
    try:
        from stat import ST_MODE, S_ISDIR
        if not os.path.lexists(answer):
            os.makedirs(answer)
        elif not S_ISDIR(os.stat(answer)[ST_MODE]):
            raise ValidationError("Invalid path (%s): path must point to a directory not a file." % answer)
        return os.path.realpath(answer)
    except OSError as e:
        raise ValidationError(e)


def check_init_script(configurator, question, answer):
    try:
        from stat import ST_MODE, S_ISDIR
        if not os.path.lexists(answer):
            os.makedirs(answer)
        elif not S_ISDIR(os.stat(answer)[ST_MODE]):
            raise ValidationError("Invalid path (%s): path must point to a directory not a file." % answer)

        with open(os.path.join(answer, 'plume'), 'w'):
            answer = os.path.realpath(answer)
            configurator.target_directory = answer
            return answer
    except OSError as e:
        raise ValidationError(e)
    except IOError as e:
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


def install_plume(accept_defaults):

    if not accept_defaults:
        return install_wizard()
    install_defaults()


def install_defaults():
    configurator = Configurator('canari.resources.templates:install_plume', '.',
                                {'non_interactive': True, 'remember_answers': False})

    configurator.variables['plume.venv'] = os.environ.get('VIRTUAL_ENV')
    if configurator.variables['plume.venv']:
        click.echo(
            'Will use the virtual environment in %r to run Plume...' % configurator.variables['plume.venv'],
            err=True
        )
    configurator.variables['plume.enable_ssl'] = 'n'
    click.echo('Installing init script to /etc/init.d...', err=True)
    configurator.variables['plume.init'] = check_init_script(configurator, '', '/etc/init.d')
    click.echo('Creating Plume root directory at /var/plume...', err=True)
    configurator.variables['plume.dir'] = check_mkdir(configurator, '', '/var/plume')
    click.echo('The PID file will be at /var/run/plume.pid...', err=True)
    configurator.variables['plume.run_dir'] = '/var/run'
    click.echo('The log files will be at /var/log/plume.log...', err=True)
    configurator.variables['plume.log_dir'] = '/var/log'
    configurator.variables['plume.user'] = check_uid(configurator, '', 'nobody')
    configurator.variables['plume.group'] = check_gid(configurator, '', 'nobody')
    click.echo('The Plume server will under UID/GID=%s/%s...' % (
        configurator.variables['plume.user'], configurator.variables['plume.group']), err=True)
    click.echo('TLS will be disabled by default...', err=True)
    configurator.variables['plume.certificate'] = ''
    configurator.variables['plume.private_key'] = ''

    configurator.ask_questions()
    configurator.render()
    finish(configurator)


def install_wizard():
    configurator = Configurator('canari.resources.templates:install_plume', '.',
                                {'non_interactive': False, 'remember_answers': False})
    configurator.ask_questions()

    if os.environ.get('VIRTUAL_ENV'):
        run_venv = click.prompt(
            "--> Canari has detected that you're running this install script from within a virtualenv.\n"
            "--> Would you like to run Plume from this virtualenv (%r) as well?" % os.environ['VIRTUAL_ENV'],
            default=True
        )
        configurator.variables['plume.venv'] = os.environ['VIRTUAL_ENV'] if run_venv else False
    else:
        configurator.variables['plume.venv'] = None

    configurator.render()
    finish(configurator)


def finish(configurator):
    click.echo('Writing canari.conf to %r...' % configurator.variables['plume.dir'], err=True)

    # move the canari.conf file from the init.d directory to the plume content directory
    src_file = os.path.join(configurator.variables['plume.init'], 'canari.conf')
    dst_file = os.path.join(configurator.variables['plume.dir'], 'canari.conf')

    if src_file != dst_file:
        with open(src_file) as src:
            with open(dst_file, 'w') as dst:
                dst.write(src.read())
        os.unlink(src_file)

    os.chmod(os.path.join(configurator.variables['plume.init'], 'plume'), 0o755)

    click.echo('done!', err=True)
