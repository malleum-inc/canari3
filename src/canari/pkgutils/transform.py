import importlib
from pkgutil import iter_modules
import string
import sys
import os
from importlib import import_module
from mrbob.configurator import Configurator
from pkg_resources import resource_listdir, resource_filename

from canari.pkgutils.maltego import MaltegoDistribution, MtzDistribution
from canari.maltego.transform import Transform
from canari.maltego.message import EntityTypeFactory
from canari.question import parse_bool
from canari.config import CanariConfigParser, OPTION_LOCAL_CONFIGS, SECTION_LOCAL, OPTION_REMOTE_PACKAGES, \
    SECTION_REMOTE, OPTION_REMOTE_CONFIGS
from canari.utils.fs import PushDir

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'TransformDistribution'
]

INCOMPATIBLE = """
!!!!!!!!!!!!!!!!!!!!!!!!!!! ERROR: NOT SUPPORTED !!!!!!!!!!!!!!!!!!!!!!!!!!!

 Starting from Maltego Radium (v3.4.0) the 'canari install-package' command
 is no longer supported. Please use the 'canari create-profile' command,
 instead. This will create an importable config file (*.mtz) which can be
 imported using the 'Import Configuration' option in Maltego. This option
 can be found by clicking on the <Maltego icon> in the top left corner of
 your Maltego window then scrolling to 'Import' then 'Import Configuration'.

 NOTE: This command will automatically install and configure the
 'canari.conf' file for you in the default location for your OS.

 EXAMPLE:

 shell> canari create-profile sploitego
 ...
 shell> ls
 sploitego.mtz <--- Import this file

!!!!!!!!!!!!!!!!!!!!!!!!!!! ERROR: NOT SUPPORTED !!!!!!!!!!!!!!!!!!!!!!!!!!!
"""


class TransformDistribution(object):
    def __init__(self, package_name):
        self._package_name = package_name.replace('.transforms', '') \
            if package_name.endswith('.transforms') else package_name

        self._package = import_module(self.name)

        print('Looking for transforms in %s...' % self.name)
        try:
            self.import_package(self._package)
        except ImportError, e:
            raise ImportError("Does not appear to be a valid canari package. "
                              "Couldn't import the '%s.transforms' package in '%s'. Error message: %s" %
                              (self.name, self.name, e))

        self._transforms = list(self.find_all_subclasses(Transform))
        self._remote_transforms = [t for t in self._transforms if t.remote]
        self._config = '%s.conf' % self.name
        self._resources = '%s.resources' % self.name
        self._package_path = os.path.abspath(self._package.__path__[0])
        self._default_prefix = os.path.join(os.path.expanduser('~'), '.canari') if self.is_site_package else os.getcwd()
        self._entities = list({v for v in EntityTypeFactory.registry.itervalues()
                               if v.__module__.startswith(self._package_name)})
        self._author = getattr(self._package, '__author__', '')
        self._email = getattr(self._package, '__email__', '')
        try:
            self._machines = [
                m for m in resource_listdir(self.get_resource_module('maltego'), '') if m.endswith('.machine')]
        except ImportError:
            self._machines = []
        if self._package_name != 'canari' and not self.has_transforms:
            raise ValueError('Error: no transforms found...')
        print('Package loaded.')

    @property
    def author(self):
        return self._author

    @property
    def author_email(self):
        return self._email

    @property
    def entities(self):
        return self._entities

    @property
    def name(self):
        return self._package_name

    @property
    def package_path(self):
        return self._package_path

    @property
    def transforms(self):
        return self._transforms

    @property
    def remote_transforms(self):
        return self._remote_transforms

    @property
    def has_remote_transforms(self):
        return bool(self.remote_transforms)

    @property
    def has_transforms(self):
        return bool(self.transforms)

    @property
    def config_file(self):
        return self._config

    @property
    def resources(self):
        return self._resources

    @property
    def is_site_package(self):
        for p in sys.path:
            if p and self.package_path.startswith(p):
                return True
        return False

    @property
    def machines(self):
        return self._machines

    @property
    def entities_file(self):
        return resource_filename(self.get_resource_module('maltego'), 'entities.mtz')

    @property
    def profile_file(self):
        return resource_filename(self.get_resource_module('maltego'), 'profile.mtz')

    @property
    def default_prefix(self):
        return self._default_prefix

    def get_resource_module(self, name):
        return '%s.%s' % (self._resources, name)

    @staticmethod
    def _write_config(src, dst, **kwargs):
        if os.path.lexists(dst) and not \
                parse_bool('%s already exists. Would you like to overwrite it?' % dst, default=False):
            return

        print ('Writing %s to %s' % (src, dst))
        with file(dst, mode='wb') as w:
            if kwargs.pop('is_template', None):
                w.write(
                        string.Template(
                                file(
                                        src
                                ).read()
                        ).substitute(**kwargs)
                )
            else:
                w.write(
                        file(
                                src
                        ).read()
                )

    @classmethod
    def _is_package_loaded(cls, pkg):
        return pkg in sys.modules

    @classmethod
    def import_package(cls, pkg):
        prefix = pkg.__name__

        if prefix == 'canari' and not cls._is_package_loaded('canari.maltego.entities'):
            import canari.maltego.entities
        else:
            for _, module_name, is_pkg in iter_modules(pkg.__path__):
                module_name = '.'.join([prefix, module_name])
                if not cls._is_package_loaded(module_name):
                    pkg = importlib.import_module(module_name)
                else:
                    pkg = sys.modules[module_name]
                if is_pkg:
                    TransformDistribution.import_package(pkg)

    def find_all_subclasses(self, cls):
        for subclass in cls.__subclasses__():
            if subclass.__module__.startswith(self._package_name) and subclass.input_type:
                yield subclass
            for sub_subclass in self.find_all_subclasses(subclass):
                yield sub_subclass

    def _update_config(self, canari_config, load=True, remote=False):
        with PushDir(os.path.dirname(canari_config)):

            config = CanariConfigParser()
            config.read(canari_config)

            configs_option = OPTION_REMOTE_CONFIGS if remote else OPTION_LOCAL_CONFIGS
            config_section = SECTION_REMOTE if remote else SECTION_LOCAL

            if configs_option not in config:
                if config_section not in config:
                    config.add_section(config_section)
                config[configs_option] = ''

            configs = config.get_as_list(configs_option)

            if load:
                if self.config_file not in configs:
                    print ('Updating %s...' % canari_config)
                    configs.append(self.config_file)
                    config[configs_option] = configs

                if remote:
                    packages = config.get_as_list(OPTION_REMOTE_PACKAGES)
                    if self.name not in packages:
                        packages.append(self.name)
                        config[OPTION_REMOTE_PACKAGES] = packages
            else:
                if self.config_file in configs:
                    print ('Updating %s...' % canari_config)
                    configs.remove(self.config_file)
                    config[configs_option] = configs

                if remote:
                    packages = config.get_as_list(OPTION_REMOTE_PACKAGES)
                    if self.name in packages:
                        packages.remove(self.name)
                        config[OPTION_REMOTE_PACKAGES] = packages

            config.write(file(canari_config, mode='wb'))

    def configure(self, install_prefix, load=True, remote=False, defaults=False, **kwargs):
        if load:
            dst = os.path.join(install_prefix, 'canari.conf')
            if os.path.lexists(dst) and not defaults and \
                    parse_bool('%s already exists. Would you like to overwrite it?' % dst, default=False):
                print 'Writing fresh copy of canari.conf to %r...' % dst
                variables = {
                    'canari.command': ' '.join(sys.argv),
                    'profile.config': self.config_file if self.name != 'canari' else '',
                    'profile.path': '${PATH},/usr/local/bin,/opt/local/bin' if os.name == 'posix' else ''
                }

                configurator = Configurator('canari.resources.templates:create_profile',
                                            install_prefix,
                                            {'non_interactive': True, 'remember_answers': True},
                                            variables=variables)
                configurator.render()
                return

        if self._package_name != 'canari':
            if load:
                package_config = resource_filename(self.get_resource_module('etc'), self.config_file)
                self._write_config(package_config, os.path.join(install_prefix, self.config_file))
            self._update_config(os.path.join(install_prefix, 'canari.conf'), load, remote)

    def _init_install_prefix(self, install_prefix):
        if not install_prefix:
            install_prefix = self.default_prefix
        if not os.path.lexists(install_prefix):
            os.makedirs(install_prefix)
        return install_prefix

    def install(self, install_prefix, distribution, configure=True, is_remote=False):
        if isinstance(distribution, basestring) or not distribution:
            distribution = MaltegoDistribution(distribution)
        if not isinstance(distribution, MtzDistribution):
            if distribution.version >= '3.4.0':
                raise ValueError(INCOMPATIBLE)
            print 'Installing transform package %s...' % self.name

        install_prefix = self._init_install_prefix(install_prefix)

        self._install_transforms(install_prefix, distribution)
        self._install_entities(distribution)
        self._install_machines(distribution)

        if configure:
            self.configure(install_prefix, remote=is_remote)

    def _install_transforms(self, prefix, distribution):
        for transform in self.transforms:
            distribution.add_transform(prefix, 'Local', transform, server='Local')

    def _install_entities(self, distribution):
        try:
            src = self.entities_file
            if not os.path.lexists(src):
                return
            mtz = MtzDistribution(src)

            for entity_file in mtz.entity_files:
                distribution.add_entity(mtz.read_file(entity_file))

            for icon_category in mtz.icon_categories:
                icon_category_dir = distribution.get_icon_category_dir(icon_category)
                for icon in mtz.get_icons_by_category(icon_category):
                    data = mtz.read_file(icon)
                    p = distribution.path_join(icon_category_dir, os.path.basename(icon))
                    print 'Installing custom icon %s to %s...' % (icon, p)
                    distribution.write_file(p, data)

        except ImportError:
            pass

    def _install_machines(self, distribution):
        try:
            package = self.get_resource_module('maltego')
            for machine in self.machines:
                src = resource_filename(package, machine)
                distribution.add_machine(machine, open(src).read())
        except ImportError:
            pass

    def uninstall(self, install_prefix, maltego_prefix=None):
        distribution = MaltegoDistribution(maltego_prefix)
        if distribution.version >= '3.4.0':
            raise ValueError("""
!!!!!!!!!!!!!!!!!!!!!!!!!!! ERROR: NOT SUPPORTED !!!!!!!!!!!!!!!!!!!!!!!!!!!

 Starting from Maltego Radium (v3.4.0) the 'canari uninstall-package'
 command is no longer supported. Please use the Maltego interface to
 uninstall packages.

!!!!!!!!!!!!!!!!!!!!!!!!!!! ERROR: NOT SUPPORTED !!!!!!!!!!!!!!!!!!!!!!!!!!!
            """)

        install_prefix = self._init_install_prefix(install_prefix)

        self._uninstall_transforms(distribution)
        self._uninstall_machines(distribution)
        self.configure(install_prefix, load=False)

    def _uninstall_machines(self, distribution):
        try:
            for machine in self.machines:
                distribution.remove_machine(machine)
        except ImportError:
            pass

    def _uninstall_transforms(self, distribution):
        for transform in self.transforms:
            distribution.remove_transform('Local', transform, server='Local')

    def create_profile(self, install_prefix, current_dir, configure=True):
        mtz = os.path.join(current_dir, '%s.mtz' % self.name)
        print('Creating profile %s...' % mtz)
        mtz = MtzDistribution(mtz, 'w')
        self.install(install_prefix, mtz, configure)
        mtz.close()

        print("""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% SUCCESS! %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 Successfully created %s. You may now import this file into
 Maltego.

 INSTRUCTIONS:
 -------------
 1. Open Maltego.
 2. Click on the home button (Maltego icon, top-left corner).
 3. Click on 'Import'.
 4. Click on 'Import Configuration'.
 5. Follow prompts.
 6. Enjoy!

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% SUCCESS! %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            """ % mtz.filename)
