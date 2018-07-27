#!/usr/bin/env python
import os
import sys

import click
import six
from past.builtins import unicode

# For some reason this function is being used in safedexml. We're going to avoid it completely.
from canari import version
from canari.commands.common import fix_binpath, fix_pypath
from canari.commands.framework import (pass_context, CanariPackage, is_new_transform, CanariGroup,
                                       parse_transform_fields, unescape_transform_value, CanariRunnerCommand,
                                       MaltegoProfile)
from canari.config import OPTION_LOCAL_PATH

six.u = unicode

from canari.mode import CanariMode

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.2'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'

__all__ = [
    'dispatcher',
    'pysudo'
]


@click.group(cls=CanariGroup)
@click.option('--debug/--no-debug', default=False)
@click.option('--working-dir', '-w', default='.', type=click.Path(exists=True))
@click.version_option(version=version, prog_name='canari')
@pass_context
def main(ctx, debug, working_dir):
    ctx.mode = CanariMode.Local
    ctx.debug = debug
    ctx.working_dir = working_dir
    fix_pypath()
    fix_binpath(ctx.config[OPTION_LOCAL_PATH])


@main.command()
def banner():
    """Lists transforms in a Canari package"""
    from canari.commands.banner import banner
    banner()


@main.command(name='create-aws-lambda')
@click.option('--bucket', '-b', metavar='<S3 bucket name>',
              help="The name of the bucket to store image and other binary resources for transforms in."
              )
@click.option('--region-name', '-r', metavar='<AWS region>', help="The region to store the S3 objects in")
@click.option('--aws-access-key-id', '-k', metavar='<AWS access key ID>', help="AWS access key ID")
@click.option('--aws-secret-access-key', '-s', metavar='<AWS secret access key>', help="AWS secret access key")
@pass_context
def create_aws_lambda(ctx, bucket, region_name, aws_access_key_id, aws_secret_access_key):
    """Creates an AWS Chalice project for deployment to AWS Lambda."""
    from canari.commands.create_aws_lambda import create_aws_lambda
    create_aws_lambda(ctx.project, bucket, region_name, aws_access_key_id, aws_secret_access_key)


@main.command(name='create-package')
@click.argument('package', nargs=1, metavar='<package name>')
def create_package(package):
    """Creates a Canari transform package skeleton."""
    from canari.commands.create_package import create_package
    create_package(package)


@main.command(name='create-profile')
@click.argument('package', nargs=1, type=CanariPackage(), default='', required=False)
@pass_context
def create_profile(ctx, package):
    """Creates an importable Maltego profile (*.mtz) file."""
    from canari.commands.create_profile import create_profile
    create_profile(ctx.config_dir, ctx.project, package)


@main.command(name='create-transform')
@click.argument('transform', nargs=1, metavar='<transform name>', callback=is_new_transform)
@pass_context
def create_transform(ctx, transform):
    """Creates a new transform in the specified directory and auto-updates dependencies."""
    from canari.commands.create_transform import create_transform
    create_transform(ctx.project, transform)


@main.command(name='debug-transform', cls=CanariRunnerCommand)
@click.argument('transform', nargs=1, metavar='<transform>')
@click.argument('params', nargs=-1, metavar='[param1 ... paramN]', required=False)
@click.argument('value', metavar='<value>', callback=unescape_transform_value)
@click.argument('fields', nargs=1, metavar='[field1=value1...#fieldN=valueN]', required=False,
                callback=parse_transform_fields)
@pass_context
def debug_transform(ctx, transform, params, value, fields):
    """Runs Canari local transforms in a terminal-friendly fashion."""
    from canari.commands.debug_transform import debug_transform
    debug_transform(transform, value, fields, params, ctx.project, ctx.config)


@main.command(name='dockerize-package')
@click.option('--host', '-H', multiple=True, metavar='[host]', help='Docker daemon socket(s) to connect to',
              required=False)
@click.option('--os', '-O', metavar='[container OS]', type=click.Choice(['alpine', 'ubuntu', 'kalilinux']),
              default='alpine')
@pass_context
def dockerize_package(ctx, os, host):
    """Creates a Docker build file pre-configured with Plume."""
    from canari.commands.dockerize_package import dockerize_package
    dockerize_package(ctx.project, os, host)


@main.command(name='generate-entities')
@click.argument('output_path', metavar='[output path]', nargs=1, required=False)
@click.option(
    '--mtz-file', '-m', metavar='<mtzfile>', help='A *.mtz file containing an export of Maltego entities.',
    default='', type=MaltegoProfile()
)
@click.option(
    '--exclude-namespace', '-e', metavar='<namespace>',
    help='Name of Maltego entity namespace to ignore. Can be defined multiple times.',
    required=False, multiple=True, default=['maltego', 'maltego.affiliation']
)
@click.option(
    '--namespace', '-n', metavar='<namespace>',
    help='Name of Maltego entity namespace to generate entity classes for. Can be defined multiple times.',
    required=False, multiple=True, default=[]
)
@click.option('--maltego-entities', '-M', help="Generate entities belonging to the 'maltego' namespace.", default=False)
@click.option('--append', '-a', help='Whether or not to append to the existing *.py file.', default=False, is_flag=True)
@click.option(
    '--entity', '-E', metavar='<entity>', help='Name of Maltego entity to generate Canari python class for.',
    required=False, multiple=True, default=[]
)
@pass_context
def generate_entities(ctx, output_path, mtz_file, exclude_namespace, namespace, maltego_entities, append, entity):
    """Converts Maltego entity definition files to Canari python classes.
    Excludes Maltego built-in entities by default."""
    from canari.commands.generate_entities import generate_entities
    generate_entities(
        ctx.project, output_path, mtz_file, exclude_namespace, namespace, maltego_entities, append, entity)


@main.command(name='generate-entities-doc')
@click.option('--out-path', '-o', metavar='<path>', default=os.getcwd(),
              help='Where the output entities.rst file will be written to.', required=False)
@click.argument('package', metavar='<package>', nargs=1, required=False, default='', type=CanariPackage())
@pass_context
def generate_entities_doc(ctx, out_path, package):
    """Create entities documentation from Canari python classes file."""
    from canari.commands.generate_entities_doc import generate_entities_doc
    generate_entities_doc(ctx.project, out_path, package)


@main.command(name='install-plume')
@click.option(
    '--accept-defaults', '-y', help='Install Plume with all the defaults in non-interactive mode.',
    default=False, is_flag=True
)
def install_plume(accept_defaults):
    """Sets up Canari Plume directory structure and configuration files."""
    from canari.commands.install_plume import install_plume
    install_plume(accept_defaults)


@main.command(name='list-transforms')
@click.argument('package', nargs=1, type=CanariPackage(), default='', required=False)
def list_transforms(package):
    """Lists transforms in a Canari package"""
    from canari.commands.list_transforms import list_transforms
    list_transforms(package)


@main.command(name='load-plume-package')
@click.argument('package', nargs=1, type=CanariPackage(), default='', required=False)
@click.option(
    '--plume-dir', '-d', metavar='[www dir]', default=os.getcwd(), help='the path where Plume is installed.'
)
@click.option(
    '--accept-defaults', '-y', help='Load Plume package with all the defaults in non-interactive mode.', default=False,
    is_flag=True
)
def load_plume_package(package, plume_dir, accept_defaults):
    """Loads a canari package into Plume."""
    from canari.commands.load_plume_package import load_plume_package
    load_plume_package(package, plume_dir, accept_defaults)


@main.command(name="remote-transform")
@click.argument('host', nargs=1, metavar='<host[:port]>')
@click.argument('transform', metavar='<transform>', nargs=1)
@click.argument('input', metavar='<entity name>=<value>', nargs=1)
@click.option(
    '--entity-field', '-f', metavar='<name>=<value>', multiple=True, default=[],
    help='The entity field name and value pair (e.g. "person.firstname=Bob"). Can be specified multiple times.'
)
@click.option(
    '--transform-parameter', '-p', metavar='<name>=<value>',
    help='Transform parameter name and value pair (e.g. "api.key=123"). Can be specified multiple times.',
    multiple=True, default=[])
@click.option(
    '--raw-output', '-r', help='Print out raw XML output instead of prettified format.', is_flag=True, default=False)
@click.option('--ssl', help='Perform request over HTTPS (default: False).', is_flag=True, default=False)
@click.option('--base-path', '-b', metavar='<base path>', default='/',
              help='The base path of the Canari transform server (default: "/").')
@click.option('--soft-limit', type=int, default=500, metavar='<soft limit>', help='Set the soft limit (default: 500)')
@click.option('--hard-limit', type=int, metavar='<hard limit>', default=10000,
              help='Set the hard limit (default: 10000)')
@click.option('--verbose', '-v', help='Enable verbose debug mode.', is_flag=True, default=False)
def remote_transform(host, transform, input, entity_field, transform_parameter, raw_output, ssl,
                     base_path, soft_limit, hard_limit, verbose):
    """Runs Canari local transforms in a terminal-friendly fashion."""
    from canari.commands.remote_transform import remote_transform
    remote_transform(host, transform, input, entity_field, transform_parameter, raw_output, ssl,
                     base_path, soft_limit, hard_limit, verbose)


@main.command(name='run-transform', cls=CanariRunnerCommand)
@click.argument('transform', nargs=1, metavar='<transform>')
@click.argument('params', nargs=-1, metavar='[param1 ... paramN]', required=False)
@click.argument('value', metavar='<value>', callback=unescape_transform_value)
@click.argument('fields', nargs=1, metavar='[field1=value1...#fieldN=valueN]', required=False,
                callback=parse_transform_fields)
@pass_context
def run_transform(ctx, transform, params, value, fields):
    """Executes the transform like it would in Maltego"""
    ctx.mode = CanariMode.LocalDispatch
    fix_pypath()
    fix_binpath(ctx.config[OPTION_LOCAL_PATH])
    from canari.commands.run_transform import run_transform
    run_transform(transform, value, fields, params, ctx.project, ctx.config)


@main.command()
@click.argument('package', metavar='<package name>', type=CanariPackage(), default='', nargs=1, required=False)
@click.option(
    '--working-dir', '-w', metavar='[working dir]', default=None,
    help="the path that will be used as the working directory for "
         "the transforms being executed in the shell (default: ~/.canari/)"
)
@click.option('--sudo', '-s', is_flag=True, default=False,
              help='Instructs the shell to automatically elevate privileges to root if necessary.')
@pass_context
def shell(ctx, package, working_dir, sudo):
    """Runs a Canari interactive python shell"""
    ctx.mode = CanariMode.LocalShellDebug
    from canari.commands.shell import shell
    shell(package, working_dir, sudo)


@main.command(name='unload-plume-package')
@click.argument('package', metavar='<package name>', type=CanariPackage(), default='', nargs=1, required=False)
@click.option(
    '--plume-dir', '-d', metavar='[www dir]', default=os.getcwd(), help='the path where Plume is installed.')
def unload_plume_package(package, plume_dir):
    """Unloads a canari package from Plume."""
    from canari.commands.unload_plume_package import unload_plume_package
    unload_plume_package(package, plume_dir)


@main.command()
def version():
    """Shows the Canari version and platform it's running on."""
    from canari.commands.version import version
    version()


@click.command(cls=CanariRunnerCommand)
@click.argument('transform', nargs=1, metavar='<transform>')
@click.argument('params', nargs=-1, metavar='[param1 ... paramN]', required=False)
@click.argument('value', metavar='<value>', callback=unescape_transform_value)
@click.argument('fields', nargs=1, metavar='[field1=value1...#fieldN=valueN]', required=False,
                callback=parse_transform_fields)
@pass_context
def dispatcher(ctx, transform, params, value, fields):
    ctx.mode = CanariMode.Local
    fix_pypath()
    fix_binpath(ctx.config[OPTION_LOCAL_PATH])
    from canari.commands.run_transform import run_transform
    run_transform(transform, value, fields, params, ctx.project, ctx.config)


def pysudo():
    from canari.easygui import passwordbox
    print(passwordbox('Please enter your password.', 'sudo', ''))


if __name__ == '__main__':
    term = os.environ.setdefault('TERM', 'dumb')
    command = os.environ.get('CANARI_COMMAND')
    sys.argv[0] = command
    if command == 'dispatcher':
        dispatcher(auto_envvar_prefix='CANARI')
    elif command == 'pysudo':
        pysudo()
    else:
        main(auto_envvar_prefix='CANARI')
