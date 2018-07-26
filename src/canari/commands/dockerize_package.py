import os
import re
import subprocess
import sys
from distutils.spawn import find_executable

import click
from mrbob.configurator import Configurator

from canari import version
from canari.question import prompt_menu
from canari.utils.fs import PushDir

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2016, Canari Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPLv3'
__version__ = '0.2'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'


def run_command(args, **kwargs):
    click.echo('Running command: %s' % ' '.join(args), err=True)
    return subprocess.Popen(args, **kwargs)


def get_output(process):
    return process.communicate()[0].decode('utf-8')


def dockerize_package(project, os_, host):
    if sys.version_info[0] > 2:
        os_ += '-py3'

    click.echo('Dockerizing %s transform package...' % project.name, err=True)

    configurator = Configurator(
        'canari.resources.templates:dockerize_package',
        project.root_dir,
        {'non_interactive': True},
        variables={'project.name': project.name, 'canari.version': version}
    )

    click.echo('Creating Dockerfile for %s...' % project.name, err=True)
    configurator.render()
    click.echo('done!', err=True)

    if not find_executable('docker'):
        click.echo("Could not find 'docker' in your system path. Please download and install Docker from "
                   "http://docker.com and rerun this command again.", err=True)
        exit(-1)

    if not host:
        if os.name == 'nt':
            host = ['']
        elif os.path.exists('/var/run/docker.sock'):
            host = ['unix:///var/run/docker.sock']

    docker_hosts = [j for sublist in [('-H', i) for i in host] for j in sublist]
    container = '%s/%s:%s' % (project.name, project.name, os_)

    if not host:
        if not find_executable('docker-machine'):
            click.echo("Could not find 'docker-machine' in your system path. Please download and install Docker "
                       "Machine from http://docker.com and rerun this command again or manually specify a Docker host "
                       "using the '-H' parameter, instead.", err=True)
            exit(-1)

        click.echo('Attempting to discover available Docker machines.', err=True)
        machines = get_output(run_command(['docker-machine', 'ls', '-q'], stdout=subprocess.PIPE)).split('\n')
        machines.remove('')

        if not machines:
            click.echo('No machines found :(\nExiting...', err=True)
            exit(-1)

        machine = prompt_menu('More than one Docker machine was detected. Which one would you like to use to'
                              'build and run this container?', machines)

        click.echo('Setting up environment for Docker machine %s' % machines[machine], err=True)

        # Inject docker environment variables
        env = get_output(run_command(['docker-machine', 'env', machines[machine]], stdout=subprocess.PIPE))
        os.environ.update(re.findall(r'export ([^=]+)="([^"]+)', env))

    with PushDir(project.root_dir):
        p = run_command(['docker'] + docker_hosts + ['build', '-t', container, '-f', 'Dockerfile-%s' % os_, '.'])
        p.communicate()
        if p.returncode:
            click.echo('An error occurred while building the Docker container.', err=True)
            exit(-1)

    if click.confirm('Would you like to run this container now?', default=False):
        port = click.prompt('Which port would you like Plume to listen on externally?',
                            default=8080, type=click.IntRange(8080, 65535))
        click.echo('Plume will be listening on http://%s:%s' %
                   (re.findall('://([^:]+)', os.environ.get('DOCKER_HOST', 'http://0.0.0.0'))[0], port), err=True)
        run_command(['docker'] + docker_hosts + ['run', '-it', '-p', '8080:%s' % port, container]).communicate()

    click.echo('done!', err=True)
