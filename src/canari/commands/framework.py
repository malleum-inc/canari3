import os
import re

import click
from mrbob.configurator import Configurator

from canari.config import load_config
from canari.mode import set_debug_mode, is_debug_exec_mode, set_canari_mode, CanariMode, get_canari_mode
from canari.pkgutils.transform import TransformDistribution
from canari.project import CanariProject
from canari.utils.fs import PushDir


unescaped_equals = re.compile(r'(?<=[^\\])=')

field_value_unescaper = re.compile(r'\\([\\#=])')

field_splitter = re.compile(r'(?<=[^\\])#')


class CanariRunnerCommand(click.Command):
    def parse_args(self, ctx, args):
        if not unescaped_equals.search(args[-1]):
            args.append('')

        super(CanariRunnerCommand, self).parse_args(ctx, args)


class CanariGroup(click.Group):

    runners = [
        'debug-transform',
        'run-transform'
    ]

    def parse_args(self, ctx, args):
        # if args[0] in self.runners and not unescaped_equals.search(args[-1]):
        #         args.append('')

        super(CanariGroup, self).parse_args(ctx, args)


class CanariContext(object):

    def __init__(self):
        self._config_dir = click.get_app_dir('canari', False, True)
        self._config_file = os.path.join(self.config_dir, 'canari.conf')
        self._config = None
        self._project = None
        self._working_dir = None

    @property
    def mode(self):
        return get_canari_mode()

    @mode.setter
    def mode(self, value):
        return set_canari_mode(value)

    @property
    def project(self):
        if not self._project:
            self._project = CanariProject()
        return self._project

    @property
    def debug(self):
        return is_debug_exec_mode()

    @debug.setter
    def debug(self, value):
        if value:
            click.echo('Debugging is enabled')
        set_debug_mode(value)

    @property
    def config_dir(self):
        if not os.path.lexists(self._config_dir):
            click.echo("Initializing Canari configuration: %s" % self._config_dir, err=True)

            configurator = Configurator(
                'canari.resources.templates:init_canari',
                self._config_dir,
                {'non_interactive': True}
            )

            configurator.ask_questions()
            configurator.render()
        return self._config_dir

    @property
    def config_file(self):
        if not self._config_file:
            self._config_file = os.path.join(self.config_dir, 'canari.conf')
        return self._config_file

    @property
    def config(self):
        if not self._config:
            click.echo("Loading Canari configuration file %r" % self.config_file, err=True)
            self._config = load_config(self.config_file)
        return self._config

    @property
    def working_dir(self):
        return self._working_dir.cwd

    @working_dir.setter
    def working_dir(self, path):
        self._working_dir = PushDir(path)
        self._working_dir.__enter__()


pass_context = click.make_pass_decorator(CanariContext, True)


class CanariPackage(click.ParamType):
    name = 'package'

    failure_message = 'required when this command is executed outside of a Canari project directory.'

    def convert(self, value, param, ctx):
        if not value:
            if not ctx or not ctx.obj:
                self.fail(self.failure_message)

            if not ctx.obj.project.is_valid:
                self.fail(self.failure_message)

            value = ctx.obj.project.name
        try:
            return TransformDistribution(value)
        except ImportError as e:
            self.fail(str(e))


def is_new_transform(ctx, param, value):
    try:
        if ctx.obj.project.transform_exists(value):
            raise click.BadParameter("Transform or module already exists with name {!r}".format(value))
    except ValueError as e:
        raise click.BadParameter(str(e))
    except AssertionError as e:
        raise click.BadArgumentUsage(str(e))
    return value


def unescape_transform_value(ctx, param, value):
    return value.replace('\\=', '=')


def unescape_field_key_value(field):
    return field_value_unescaper.sub(r'\1', field)


def parse_transform_fields(ctx, param, value):
    fields = {}
    if value:
        for field in re.split(r'(?<=[^\\])#', value):
            k, v = unescaped_equals.split(field, 1)
            fields[unescape_field_key_value(k)] = unescape_field_key_value(v)
    return fields


class MaltegoProfile(click.ParamType):
    name = 'package'

    failure_message = 'required when this command is executed outside of a Canari project directory.'

    def convert(self, value, param, ctx):
        if not value:
            if not ctx or not ctx.obj:
                self.fail(self.failure_message)

            if not ctx.obj.project.is_valid:
                self.fail(self.failure_message)

            value = ctx.obj.project.entities_mtz

        if not os.path.lexists(value):
            self.fail('Maltego profile export does not exist: {}'.format(ctx.obj.project.entities_mtz))

        return value
