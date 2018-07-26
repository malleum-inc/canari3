from __future__ import print_function

from future.builtins import bytes

import os
import re
import sys
import tempfile
import time
from distutils.version import LooseVersion
from importlib import import_module
from zipfile import ZipFile, ZIP_STORED

from six import string_types
from safedexml import Model

from canari.maltego.configuration import (TransformSettings, CmdLineTransformPropertySetting, InputConstraint, Set,
                                          CmdParmTransformPropertySetting, CmdCwdTransformPropertySetting,
                                          CmdDbgTransformPropertySetting, MaltegoTransform,
                                          CmdLineTransformProperty, CmdCwdTransformProperty, CmdDbgTransformProperty,
                                          CmdParmTransformProperty, TransformSet, Transform, MaltegoServer, Protocol,
                                          Authentication, EntityCategory, Properties, attributes, fileobject, attr,
                                          MaltegoEntity)
from canari.question import prompt_menu
from canari.utils.common import find_dispatcher

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'

__all__ = [
    'MaltegoDistribution',
    'MtzDistribution'
]


class MaltegoVersion:
    Radium = '3.2.0'
    Tungsten = '3.4.0'
    Carbon = '3.5.0'
    Chlorine = '3.6.0'


class MaltegoDistribution(object):

    def __init__(self, maltego_prefix=None, **kwargs):
        self._maltego_prefix = maltego_prefix if maltego_prefix else self._detect_settings_dir()
        self._maltego_config_dir = self.path_join(self.maltego_prefix, 'config', 'Maltego')
        self._seeds_dir = self.path_join(self.maltego_config_dir, 'Seeds')
        self._servers_dir = self.path_join(self.maltego_config_dir, 'Servers')
        self._entities_dir = self.path_join(self.maltego_config_dir, 'Entities')
        self._machines_dir = self.path_join(self.maltego_config_dir, 'Machines')
        self._icons_dir = self.path_join(self.maltego_config_dir, 'Icons')
        self._viewlets_dir = self.path_join(self.maltego_config_dir, 'Viewlets')
        self._transform_sets_dir = self.path_join(self.maltego_config_dir, 'TransformSets')
        self._transform_repositories_dir = self.path_join(self.maltego_config_dir, 'TransformRepositories')
        version = os.path.basename(self.maltego_prefix)
        self._version = LooseVersion(version[1:]) if version.startswith('v') else LooseVersion(version)
        self._machine_nbattr = self._get_machine_nbattr()

    @property
    def maltego_prefix(self):
        return self._maltego_prefix

    def _get_dir(self, dir_name, subdir_name=None, create=True):
        path = dir_name
        if subdir_name:
            path = os.path.join(dir_name, subdir_name)
        if not os.path.lexists(path):
            if create:
                os.makedirs(path, 0o755)
            else:
                raise OSError('Path does not exist: %r' % path)
        return path

    @property
    def viewlets_dir(self):
        return self._viewlets_dir

    @property
    def icons_dir(self):
        return self._icons_dir

    @property
    def icon_categories(self):
        return [p for p in os.listdir(self.icons_dir) if os.path.isdir(os.path.join(self.icons_dir, p))]

    @property
    def icon_files(self):
        return [os.path.join(p, i) for p, d, f in os.walk(self.icons_dir) for i in f if i]

    @property
    def icons(self):
        return self.icon_files

    @property
    def servers_dir(self):
        return self._servers_dir

    @property
    def server_files(self):
        return [os.path.join(self.servers_dir, s) for s in os.listdir(self.servers_dir) if s.endswith('.tas')]

    @property
    def servers(self):
        return self.server_files

    @property
    def maltego_config_dir(self):
        return self._maltego_config_dir

    @property
    def seeds_dir(self):
        return self._seeds_dir

    @property
    def entities_dir(self):
        return self._entities_dir

    @property
    def machine_files(self):
        return [os.path.join(self.machines_dir, m) for m in os.listdir(self.machines_dir) if m.endswith('.machine')]

    @property
    def machines(self):
        return self.machine_files

    @property
    def entity_files(self):
        return [os.path.join(p, i) for p, d, f in os.walk(self.entities_dir) for i in f if i.endswith('.entity')]

    @property
    def entities(self):
        return self.entity_files

    @property
    def transform_files(self):
        return [(os.path.join(p, t), '%ssettings' % os.path.join(p, t)) for p, d, f in
                os.walk(self.transform_repositories_dir) for t in f if t.endswith('.transform')]

    @property
    def transforms(self):
        return self.transform_files

    @property
    def transform_uuids(self):
        return [t.replace('.transform', '') for p, d, f in
                os.walk(self.transform_repositories_dir) for t in f if t.endswith('.transform')]

    @property
    def entity_categories(self):
        return [p for p in os.listdir(self.entities_dir)
                if os.path.isdir(os.path.join(self.entities_dir, p))]

    @property
    def transform_sets(self):
        return [p for p in os.listdir(self.transform_sets_dir)
                if os.path.isdir(os.path.join(self.transform_sets_dir, p))]

    @property
    def transform_repositories_dir(self):
        return self._transform_repositories_dir

    @property
    def transform_repositories(self):
        return [p for p in os.listdir(self.transform_repositories_dir)
                if os.path.isdir(os.path.join(self.transform_repositories_dir, p))]

    @property
    def transform_sets_dir(self):
        return self._transform_sets_dir

    @property
    def machines_dir(self):
        return self._machines_dir

    @property
    def seed_files(self):
        return [os.path.join(self.seeds_dir, s) for s in os.listdir(self.seeds_dir) if s.endswith('.seed')]

    @property
    def seeds(self):
        return self.seed_files

    @property
    def version(self):
        return self._version

    def get_transform_repository_dir(self, transform_repository_name):
        return self._get_dir(self.transform_repositories_dir, transform_repository_name,
                             False if self.version >= MaltegoVersion.Tungsten else True)

    def get_icon_category_dir(self, icon_category_name):
        return self._get_dir(self.icons_dir, icon_category_name,
                             False if self.version >= MaltegoVersion.Tungsten else True)

    def get_entity_category_dir(self, entity_category_name):
        return self._get_dir(self.entities_dir, entity_category_name,
                             False if self.version >= MaltegoVersion.Tungsten else True)

    def get_transform_set_dir(self, transform_set_name):
        return self._get_dir(self.transform_sets_dir, transform_set_name,
                             False if self.version >= MaltegoVersion.Tungsten else True)

    def add_server(self, server_name, **kwargs):
        pass

    def add_transform_to_server(self, server_name, transform_id):
        pass

    def remove_transform_from_server(self, server_name, transform_id):
        pass

    def add_transform_set(self, transform_set_name):
        if self.version >= MaltegoVersion.Tungsten:
            raise NotImplementedError('This version of Maltego uses encrypted configuration files and therefore does '
                                      'not support direct management of transform sets.')
        self.get_transform_set_dir(transform_set_name)

    def add_transform_repository(self, transform_repository_name):
        if self.version >= MaltegoVersion.Tungsten:
            raise NotImplementedError('This version of Maltego uses encrypted configuration files and therefore does '
                                      'not support direct management of transform repositories.')
        self.get_transform_repository_dir(transform_repository_name)

    def add_entity_category(self, entity_category_name):
        if self.version >= MaltegoVersion.Tungsten:
            raise NotImplementedError('This version of Maltego uses encrypted configuration files and therefore does '
                                      'not support direct management of entity categories.')
        self.get_entity_category_dir(entity_category_name)

    def add_icon_category(self, icon_category_name):
        if self.version >= MaltegoVersion.Tungsten:
            raise NotImplementedError('This version of Maltego uses encrypted configuration files and therefore does '
                                      'not support direct management of icon categories.')
        self.get_entity_category_dir(icon_category_name)

    def get_transforms_by_repository(self, transform_repository_name):
        return [t for t in self.transforms
                if t[0].startswith(self.get_transform_repository_dir(transform_repository_name))]

    def get_icons_by_category(self, icon_category_name):
        return [i for i in self.icon_files if i.startswith(self.get_icon_category_dir(icon_category_name))]

    def _iter_settings_dir(self, maltego_base_dir):
        vs = [i for i in os.listdir(maltego_base_dir) if os.path.isdir(os.path.join(maltego_base_dir, i)) and
                                                         os.path.isdir(os.path.join(maltego_base_dir, i, 'config'))]
        if len(vs) == 1:
            return os.path.join(maltego_base_dir, vs[0])
        elif vs:
            print('Multiple versions of Maltego detected: ', file=sys.stderr)
            r = prompt_menu('Please select which version you wish to use', ['Maltego %s' % i for i in vs])
            return os.path.join(maltego_base_dir, vs[int(r)])
        print('Could not automatically find Maltego\'s settings directory. '
              'Use the -w parameter to specify its location, instead.', file=sys.stderr)

    def _detect_settings_dir(self):
        if sys.platform.startswith('linux'):
            return self._iter_settings_dir(os.path.join(os.path.expanduser('~'), '.maltego'))
        elif sys.platform == 'darwin':
            return self._iter_settings_dir(
                os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'maltego')
            )
        elif sys.platform == 'win32':
            return self._iter_settings_dir(os.path.join(os.environ['APPDATA'], '.maltego'))
        raise NotImplementedError('Unknown or unsupported OS: %r' % sys.platform)

    def add_transform_to_set(self, transform_id, transform_set):
        self.add_transform_set(transform_set)
        self.write_file(self.path_join(self.get_transform_set_dir(transform_set), transform_id), '')

    def remove_transform_from_set(self, transform_id, transform_set):
        transform_set_dir = self.get_transform_set_dir(transform_set)
        path = os.path.join(transform_set_dir, transform_id)
        self.remove_file(path)
        if not os.listdir(transform_set_dir):
            os.rmdir(transform_set_dir)

    def _get_module_author(self, module_name):
        return getattr(import_module(module_name), '__author__', '')

    def add_transform(self, working_dir, transform_repository, transform, server=None):
        transform_repository_dir = self.get_transform_repository_dir(transform_repository)

        py_name = '.'.join([transform.__module__, transform.__name__])
        author = transform.author
        transform_id = transform.name
        input_set = transform.transform_set
        input_entity = transform.input_type

        if transform.name in self.transform_uuids:
            print('WARNING: Previous declaration of %s in transform %s. Overwriting...' % (transform_id, py_name),
                  file=sys.stderr)
        else:
            print('Installing transform %s from %s...' % (transform_id, py_name), file=sys.stderr)

        sets = None
        if input_set:
            sets = Set(name=input_set)
            self.add_transform_to_set(transform_id, input_set)

        if server:
            self.add_transform_to_server(server, transform_id)

        transform_def = MaltegoTransform(
            name=transform_id,
            displayname=transform.display_name,
            author=author,
            description=transform.description,
            properties=(
                Properties() +
                CmdLineTransformProperty() +
                CmdCwdTransformProperty() +
                CmdDbgTransformProperty() +
                CmdParmTransformProperty()
            ),
            input=[InputConstraint(type=input_entity._type_)],
            sets=[sets]
        )

        self.write_file(
            self.path_join(transform_repository_dir, '%s.transform' % transform_id),
            transform_def
        )

        if not transform_def.sets:
            print('WARNING: Transform does not appear to be part of any Transform Sets (Perhaps an error?).',
                  file=sys.stderr)

        transform_settings_def = TransformSettings(properties=[
            CmdLineTransformPropertySetting(find_dispatcher()),
            CmdParmTransformPropertySetting(py_name),
            CmdCwdTransformPropertySetting(working_dir),
            CmdDbgTransformPropertySetting(transform.debug)
        ])

        self.write_file(
            self.path_join(transform_repository_dir, '%s.transformsettings' % transform_id),
            transform_settings_def
        )

    def remove_transform(self, transform_repository, transform, server=None):
        spec = transform.dotransform
        transform_repository_dir = self.get_transform_repository_dir(transform_repository)

        for transform_id, (input_set, input_entity) in zip(spec.uuids, spec.inputs):
            print('Removing %s from %s...' % (transform_id, transform_repository_dir), file=sys.stderr)
            self.remove_file(self.path_join(transform_repository_dir, '%s.transform' % transform_id))
            self.remove_file(self.path_join(transform_repository_dir, '%s.transformsettings' % transform_id))
            self.remove_transform_from_set(transform_id, input_set)
            if server:
                self.remove_transform_from_server(server, transform_id)

    def _get_machine_nbattr(self):
        nbattr = attributes()
        if self.version >= MaltegoVersion.Tungsten:
            return nbattr
        f = self.path_join(self.machines_dir, '.nbattrs')
        if os.path.exists(f):
            data = open(f).read()
            if data:
                nbattr = nbattr.parse(data)
        return nbattr

    def _parse_machine_script(self, contents):
        machine_sig = re.search('machine\s*\n*\((.+)\)\s*\n*{\s*\n*start\s*\n*{', contents, re.MULTILINE | re.DOTALL)
        if not machine_sig:
            return
        props = dict(re.findall(r'(?:(\w+)\s*:\s*)?["\']([^"\']+)["\']', machine_sig.groups()[0]))
        props['name'] = props.pop('')
        return props

    def remove_machine(self, filename):
        if self.version >= MaltegoVersion.Tungsten:
            raise NotImplementedError('This version of Maltego uses encrypted files and therefore does '
                                      'not support direct management of machine files.')
        filename = os.path.basename(filename)
        name = filename.replace('.machine', '')

        print('Uninstalling %s from %s...' % (filename, self.machines_dir), file=sys.stderr)
        if name in self._machine_nbattr.fileobjects:
            del self._machine_nbattr.fileobjects[name]

        self.remove_file(os.path.join(self.machines_dir, filename))

    def add_machine(self, filename, contents):
        if self.version >= MaltegoVersion.Tungsten:
            raise NotImplementedError('This version of Maltego uses encrypted files and therefore does '
                                      'not support direct management of machine files.')
        props = self._parse_machine_script(contents)
        if not props:
            return
        if props['name'] not in self._machine_nbattr.fileobjects:
            f = fileobject(name=props['name'])
            self._machine_nbattr += f
            for n, v in props.items():
                f += attr(name=n, stringvalue=v)
            f += attr(name='enabled', boolvalue=True)
            f += attr(name='readonly', boolvalue=False)

        dst = self.path_join(self.machines_dir, os.path.basename(filename))
        print('Installing machine %s to %s...' % (filename, dst), file=sys.stderr)
        self.write_file(dst, contents)

    def add_entity(self, entity):
        if isinstance(entity, string_types):
            entity = MaltegoEntity.parse(entity)
        if not isinstance(entity, MaltegoEntity):
            raise TypeError('Expected str or MaltegoEntity, not %s', type(entity).__name__)
        entity_category_dir = self.get_entity_category_dir(entity.category)
        entity_filename = '%s.entity' % self.path_join(entity_category_dir, entity.id)
        print('Installing entity %s to %s...' % (entity.id, entity_filename), file=sys.stderr)
        self.write_file(entity_filename, entity.render(fragment=True, pretty=True))

    def path_join(self, *args):
        return os.path.join(*args)

    def write_file(self, filename, contents):
        if self.version >= MaltegoVersion.Tungsten:
            raise NotImplementedError('This version of Maltego uses encrypted files and therefore does '
                                      'not support direct management of any files within the configuration directory.')
        with open(filename, 'w') as f:
            if isinstance(contents, Model):
                f.write(contents.render(fragment=True, pretty=True))
            else:
                f.write(contents)

    def read_file(self, filename):
        return open(filename).read()

    def _write_pending(self):
        nbattrs = self.path_join(self.machines_dir, '.nbattrs')
        with open(nbattrs, mode='w') as f:
            f.write(self._machine_nbattr.render(fragment=True, pretty=True))

    def remove_file(self, filename):
        if os.path.lexists(filename):
            os.unlink(filename)

    def __del__(self):
        if not hasattr(self, '_version') or self.version >= MaltegoVersion.Tungsten:
            return
        self._write_pending()


class MtzZipFile(object):

    def __init__(self, file_, mode="r", compression=ZIP_STORED, allowZip64=False, pwd=None):
        self._zipfile = None
        self.mode = mode
        self.filename = file_
        self._is_closed = False
        self.compression = ZIP_STORED
        self.allowZip64 = allowZip64
        if mode == "r":
            self._zipfile = ZipFile(file_, mode, compression, allowZip64)
        else:
            self._root_dir = tempfile.mkdtemp() + os.path.sep
            if self.mode == 'a':
                ZipFile(file_, 'r').extractall(self._root_dir, pwd)

    def namelist(self):
        if self._is_closed:
            raise RuntimeError('Attempt to read ZIP archive that was already closed')
        if self.mode == 'r':
            return self._zipfile.namelist()
        namelist = []
        for p, d, f in os.walk(self._root_dir):
            if f:
                for f_ in f:
                    f_ = os.path.join(p, f_)
                    namelist.append(self._get_archive_file(f_))
        return namelist

    def writestr(self, zinfo_or_arcname, bytes_):
        if isinstance(bytes_, string_types):
            bytes_ = bytes(bytes_, 'utf8')
        if self._is_closed:
            raise RuntimeError('Attempt to read ZIP archive that was already closed')
        if self.mode == 'r':
            return self._zipfile.writestr(zinfo_or_arcname, bytes_)
        realpath = self._get_real_file(zinfo_or_arcname)
        realdir = os.path.dirname(realpath)
        if not os.path.isdir(realdir):
            os.makedirs(realdir)
        with open(realpath, mode='wb') as f:
            f.write(bytes_)

    def removefile(self, zinfo_or_arcname):
        if self._is_closed:
            raise RuntimeError('Attempt to remove file from ZIP archive that was already closed')
        if self.mode == 'r':
            return self._zipfile.writestr(zinfo_or_arcname, bytes)
        realpath = self._get_real_file(zinfo_or_arcname)
        if os.path.lexists(realpath):
            os.unlink(realpath)

    def read(self, name, pwd=None):
        if self._is_closed:
            raise RuntimeError('Attempt to read ZIP archive that was already closed')
        if self.mode == 'r':
            return self._zipfile.read(name, pwd)
        with open(self._get_real_file(name)) as f:
            return f.read()

    def _get_real_file(self, name):
        if sys.platform == 'win32':
            name = name.replace('/', os.path.sep)
        return os.path.join(self._root_dir, name)

    def _get_archive_file(self, name):
        name = name.replace(self._root_dir, '', 1)
        if sys.platform == 'win32':
            name = name.replace(os.path.sep, '/')
        return name

    def close(self):
        if self._is_closed or self.mode == 'r':
            return
        self._is_closed = True
        with ZipFile(self.filename, mode='w', compression=self.compression, allowZip64=self.allowZip64) as z:
            for p, d, f in os.walk(self._root_dir):
                if f:
                    for f_ in f:
                        name = os.path.join(p, f_)
                        z.write(name, self._get_archive_file(name))
                        os.unlink(name)

    def __del__(self):
        if not self._is_closed:
            self.close()


class MtzDistribution(MtzZipFile, MaltegoDistribution):

    def __init__(self, file_, mode="r", compression=ZIP_STORED, allowZip64=False):
        super(MtzDistribution, self).__init__(file_, mode, compression, allowZip64)
        self._maltego_config_dir = self.filename
        self._maltego_prefix = ''
        self._icons_dir = 'Icons'
        self._seeds_dir = 'Seeds'
        self._servers_dir = 'Servers'
        self._viewlets_dir = 'Viewlets'
        self._entities_dir = 'Entities'
        self._machines_dir = 'Machines'
        self._transform_sets_dir = 'TransformSets'
        self._transform_repositories_dir = 'TransformRepositories'
        self._version = NotImplemented
        self._transform_sets = {}
        self._servers = {}
        self._init_transform_sets()
        self._init_servers()

    def _init_servers(self):
        for s in self.namelist():
            if s.endswith('.tas'):
                self._append_server(s)

    def _append_server(self, s):
        s = MaltegoServer.parse(self.read(s))
        self.add_server(
            s.name,
            enabled=s.enabled,
            description=s.description,
            url=s.url,
            lastsync=s.lastsync,
            protocol=s.protocol.version,
            authentication=s.authentication.type,
            transforms=[t.name for t in s.transforms]
        )

    def _init_transform_sets(self):
        for s in self.namelist():
            if s.endswith('.set'):
                self._append_transform_set(s)

    def _append_transform_set(self, s):
        s = TransformSet.parse(self.read(s))
        self.add_transform_set(
            s.name,
            description=s.description,
            transforms=[t.name for t in s.transforms]
        )

    @property
    def icon_files(self):
        return [i for i in self.namelist() if i.startswith('Icons/')]

    @property
    def server_files(self):
        return [self._servers[s]['filename'] for s in self._servers]

    @property
    def entity_files(self):
        return [e for e in self.namelist() if e.endswith('.entity')]

    @property
    def transform_repositories(self):
        return self._match_one(r'TransformRepositories/(.+)?/.*')

    @property
    def transform_sets(self):
        return self._transform_sets.keys()

    @property
    def transform_set_files(self):
        return [self._transform_sets[t]['filename'] for t in self._transform_sets]

    @property
    def entity_categories(self):
        return self._match_one(r'EntityCategories/(.+)?\.category')

    @property
    def machine_files(self):
        return [m for m in self.namelist() if m.endswith('.machine')]

    @property
    def seed_files(self):
        return [s for s in self.namelist() if s.endswith('.seed')]

    @property
    def icon_categories(self):
        return self._match_one(r'Icons/(.+)?/.*', ['Custom'])

    @property
    def transform_files(self):
        return [(t, '%ssettings' % t) for t in self.namelist() if t.endswith('.transform')]

    @property
    def transform_uuids(self):
        return self._match_one(r'TransformRepositories/.*?/(.+)?\.transform')

    def _match_one(self, regex, l=None):
        if l is None:
            l = []
        for r in self.namelist():
            m = re.match(regex, r)
            if not m:
                continue
            category = m.groups()[0]
            if category not in l:
                l.append(category)
        return l

    def get_icons_by_category(self, icon_category_name):
        if icon_category_name == 'Custom':
            return [i for i in self.icon_files if i.count('/') == 1]
        return [i for i in self.icon_files if i.startswith(self.get_icon_category_dir(icon_category_name))]

    def get_transform_repository_dir(self, transform_repository_name):
        return self.path_join(self.transform_repositories_dir, transform_repository_name)

    def get_entity_category_dir(self, entity_category_name):
        name = '/'.join(['EntityCategories', entity_category_name
                        if entity_category_name.endswith('.set') else '%s.set' % entity_category_name])
        if name not in self.transform_set_files:
            self.write_file(name, EntityCategory(name=entity_category_name))
        return name

    def get_transform_set_dir(self, transform_set_name):
        return '/'.join([self.transform_sets_dir,
                         transform_set_name if transform_set_name.endswith('.set') else '%s.set' % transform_set_name])

    def get_icon_category_dir(self, icon_category_name):
        return self.icons_dir if icon_category_name == 'Custom' else self.path_join(self.icons_dir, icon_category_name)

    def add_transform_set(self, transform_set_name, **kwargs):
        transforms = kwargs.get('transforms', [])
        if transform_set_name not in self._transform_sets:
            self._transform_sets[transform_set_name] = dict(
                filename=self.get_transform_set_dir(transform_set_name),
                description=kwargs.get('description', ''),
                transforms=transforms
            )
        elif transforms:
            for t in transforms:
                if t not in self._transform_sets[transform_set_name]['transforms']:
                    self._transform_sets[transform_set_name]['transforms'].append(t)

    def add_transform_repository(self, transform_repository_name):
        if self.mode == 'r':
            raise RuntimeError('Adding a transform repository requires mode "w" or "a"')
        self.get_transform_repository_dir(transform_repository_name)

    def add_entity_category(self, entity_category_name):
        if self.mode == 'r':
            raise RuntimeError('Adding an entity category requires mode "w" or "a"')
        self.get_entity_category_dir(entity_category_name)

    def add_icon_category(self, icon_category_name):
        if self.mode == 'r':
            raise RuntimeError('Adding an icon category requires mode "w" or "a"')
        self.get_icon_category_dir(icon_category_name)

    def write_file(self, zinfo_or_arcname, contents):
        if '\\' in zinfo_or_arcname:
            zinfo_or_arcname.replace('\\', '/')
        if isinstance(contents, Model):
            contents = contents.render(fragment=True, pretty=True)
        self.writestr(zinfo_or_arcname, contents)

    def add_transform_to_set(self, transform_id, transform_set):
        self.add_transform_set(transform_set)
        if transform_id not in self._transform_sets[transform_set]['transforms']:
            self._transform_sets[transform_set]['transforms'].append(transform_id)

    def _write_pending(self):
        # Write pending transform sets
        for transform_set, transform_set_def in self._transform_sets.items():
            transform_set_xml = TransformSet(
                name=transform_set,
                description=transform_set_def['description'],
                transforms=[Transform(name=transform) for transform in transform_set_def['transforms']]
            )
            print('Writing transform set %s to %s...' % (transform_set, self.filename), file=sys.stderr)
            self.write_file(transform_set_def['filename'], transform_set_xml)

        # Write pending server definitions
        for s, server_def in self._servers.items():
            server = MaltegoServer(
                name=s,
                enabled=server_def['enabled'],
                description=server_def['description'],
                url=server_def['url'],
                lastsync=server_def['lastsync'],
                protocol=Protocol(version=server_def['protocol']),
                authentication=Authentication(type_=server_def['authentication']),
                transforms=[Transform(name=transform) for transform in server_def['transforms']]
            )
            print('Writing server %s to %s' % (s, self.filename), file=sys.stderr)
            self.write_file(server_def['filename'], server)

    def add_server(self, server_name, **kwargs):
        transforms = kwargs.get('transforms', [])
        if server_name not in self._servers:
            self._servers[server_name] = dict(
                filename=self.path_join(self.servers_dir, '%s.tas' % server_name),
                enabled=kwargs.get('enabled', True),
                description=kwargs.get('description', 'Local transforms hosted on this machine'),
                url=kwargs.get('url', 'http://localhost'),
                lastsync=kwargs.get('lastsync', time.strftime('%Y-%m-%d')),
                protocol=kwargs.get('protocol', '0.0'),
                authentication=kwargs.get('type_', 'none'),
                transforms=transforms
            )
        elif transforms:
            for t in transforms:
                if t not in self._servers[server_name]['transforms']:
                    self._servers[server_name]['transforms'].append(t)

    def add_transform_to_server(self, server_name, transform_id):
        self.add_server(server_name)
        if transform_id not in self._servers[server_name]['transforms']:
            self._servers[server_name]['transforms'].append(transform_id)

    def remove_transform_from_server(self, server_name, transform_id):
        if transform_id in self._servers[server_name]['transforms']:
            self._servers[server_name]['transforms'].remove(transform_id)

    def add_machine(self, name, contents):
        print('Writing machine %s to %s...' % (name, self.filename), file=sys.stderr)
        self.write_file(self.path_join(self.machines_dir, name), contents)
        self.write_file(self.path_join(self.machines_dir, name.replace('.machine', '.properties')), 'enabled=true')

    def remove_machine(self, filename):
        print('Removing %s from %s...' % (filename, self.machines_dir), file=sys.stderr)
        path = self.path_join(self.machines_dir, os.path.basename(filename))
        self.remove_file(path)
        self.remove_file(path.replace('.machine', '.properties'))

    def remove_file(self, filename):
        self.removefile(filename)

    def merge(self, mtz_file):
        if not isinstance(mtz_file, MtzDistribution):
            raise TypeError('Expected MtzDistribution object got %s instead.' % type(mtz_file).__name__)
        for f in mtz_file.namelist():
            print('Writing %s to %s...' % (f, mtz_file.filename), file=sys.stderr)
            if re.match(r'.*?/(.+)?\.(entity|category|transform(settings)?|mtvs|properties|machine|seed)$', f):
                self.write_file(f, mtz_file.read_file(f))
            elif f.endswith('.tas'):
                self._append_server(mtz_file.read_file(f))
            elif f.endswith('.set'):
                self._append_transform_set(mtz_file.read_file(f))

    def add_entity(self, entity):
        if isinstance(entity, string_types):
            entity = MaltegoEntity.parse(entity)
        if not isinstance(entity, MaltegoEntity):
            raise TypeError('Expected str or MaltegoEntity, not %s', type(entity).__name__)
        self.add_entity_category(entity.category)
        entity_filename = '%s.entity' % self.path_join(self.entities_dir, entity.id)
        print('Installing entity %s to %s...' % (entity.id, entity_filename), file=sys.stderr)
        self.write_file(entity_filename, entity.render(fragment=True, pretty=True))

    def path_join(self, *args):
        return '/'.join(args)

    def read_file(self, filename, decode=True):
        if decode:
            return self.read(filename).decode('utf8')
        return self.read(filename)

    def close(self):
        if self.mode != 'r':
            self._write_pending()
        super(MtzDistribution, self).close()
