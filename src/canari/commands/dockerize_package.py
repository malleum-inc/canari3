from __future__ import print_function

import os
import subprocess

import re
import sys

from canari import question, __version__ as version
from mrbob.configurator import Configurator

from canari.project import CanariProject
from canari.utils.fs import PushDir
from canari.commands.common import canari_main
from canari.commands.framework import SubCommand, Argument
from distutils.spawn import find_executable

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2016, Canari Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPLv3'
__version__ = '0.2'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def run_command(args, **kwargs):
    print('Running command: %s' % ' '.join(args), file=sys.stderr)
    return subprocess.Popen(args, **kwargs)


def get_output(process):
    return process.communicate()[0].decode('utf-8')


@SubCommand(
    canari_main,
    help='Creates a Docker build file pre-configured with Plume.',
    description='Creates a Docker build file that can be used to run remote transforms using Plume.'
)
@Argument(
    '-H',
    '--host',
    metavar='[host]',
    action='append',
    default=[],
    help='Docker daemon socket(s) to connect to'
)
@Argument(
    '-O',
    '--os',
    metavar='[container OS]',
    choices=['alpine', 'ubuntu', 'kalilinux'],
    default='alpine'
)
def dockerize_package(args):
    if sys.version_info[0] > 2:
        args.os += '-py3'

    project = CanariProject()

    print('Dockerizing %s transform package...' % project.name, file=sys.stderr)

    configurator = Configurator(
            'canari.resources.templates:dockerize_package',
            project.root_dir,
            {'non_interactive': True},
            variables={'project.name': project.name, 'canari.version': version}
    )

    print('Creating Dockerfile for %s...' % project.name, file=sys.stderr)
    configurator.render()
    print('done!', file=sys.stderr)

    if not find_executable('docker'):
        print("""Could not find 'docker' in your system path. Please download and install Docker from http://docker.com
        and rerun this command again.
        """, file=sys.stderr)
        exit(-1)

    if not args.host:
        if os.name == 'nt':
            args.host = ['']
        elif os.path.exists('/var/run/docker.sock'):
            args.host = ['unix:///var/run/docker.sock']

    docker_hosts = [j for sublist in [('-H', i) for i in args.host] for j in sublist]
    container = '%s/%s:%s' % (project.name, project.name, args.os)

    if not args.host:
        if not find_executable('docker-machine'):
            print("""Could not find 'docker-machine' in your system path. Please download and install Docker Machine from
            http://docker.com and rerun this command again or manually specify a Docker host using the '-H' parameter,
            instead.
            """, file=sys.stderr)
            exit(-1)

        print('Attempting to discover available Docker machines.', file=sys.stderr)
        machines = get_output(run_command(['docker-machine', 'ls', '-q'],stdout=subprocess.PIPE)).split('\n')
        machines.remove('')

        if not machines:
            print('No machines found :(\nExiting...', file=sys.stderr)
            exit(-1)

        machine = question.parse_int('More than one Docker machine was detected. Which one would you like to use to'
                                     'build and run this container?', machines) if len(machines) != 1 else 0

        print('Setting up environment for Docker machine %s' % machines[machine], file=sys.stderr)

        # Inject docker environment variables
        env = get_output(run_command(['docker-machine', 'env', machines[machine]], stdout=subprocess.PIPE))
        os.environ.update(re.findall(r'export ([^=]+)="([^"]+)', env))

    with PushDir(project.root_dir):
        p = run_command(['docker'] + docker_hosts + ['build', '-t', container, '-f', 'Dockerfile-%s' % args.os, '.'])
        p.communicate()
        if p.returncode:
            print('An error occurred while building the Docker container.', file=sys.stderr)
            exit(-1)

    if question.parse_bool('Would you like to run this container now?'):
        port = question.parse_int_range('Which port would you like Plume to listen on externally?', 0, 65535, 8080)
        print('Plume will be listening on http://%s:%s' %
              (re.findall('://([^:]+)', os.environ.get('DOCKER_HOST', 'http://0.0.0.0'))[0], port), file=sys.stderr)
        run_command(['docker'] + docker_hosts + ['run', '-it', '-p', '8080:%s' % port, container]).communicate()

    print('done!', file=sys.stderr)
