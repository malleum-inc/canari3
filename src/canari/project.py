import getpass
import os

from datetime import date
from importlib import import_module

import sys

import canari
from mrbob.parsing import parse_config

from canari.utils.fs import PushDir

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2016, canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = []


class CanariProject(object):

    marker = '.canari'

    def __init__(self, path=None):
        if not path:
            path = os.getcwd()

        try:
            self._tree = self.project_tree(path)
            self._in_project = True
            self._configuration = parse_config(os.path.join(self.root_dir, '.mrbob.ini'))
            sys.path.insert(0, self.src_dir)
        except ValueError:
            self._tree = dict(
                    root=path,
                    src=path,
                    pkg=path,
                    resources=path,
                    transforms=path
            )
            self._in_project = False
            self._configuration = {'variables': {'created.year': date.today().year, 'author.name': getpass.getuser(),
                                                 'project.name': 'canari', 'canari.version': canari.__version__,
                                                 'author.email': 'transformer@canariframework.com',
                                                 'project.description': '', 'entity.base_name': 'Entity'}}

    @property
    def entities_module(self):
        name = self.name
        return import_module('canari.maltego.entities' if name == 'canari' else '%s.transforms.common.entities' % name)

    @property
    def name(self):
        return self._configuration['variables']['project.name']

    @property
    def root_dir(self):
        return self._tree.get('root')

    @property
    def src_dir(self):
        return self._tree.get('src')

    @property
    def resources_dir(self):
        return self._tree.get('resources')

    @property
    def transforms_dir(self):
        return self._tree.get('transforms')

    @property
    def common_dir(self):
        return self._tree.get('common')

    @property
    def entities_mtz(self):
        return os.path.join(self.resources_dir, 'maltego', 'entities.mtz')

    @property
    def entities_py(self):
        return os.path.join(self.common_dir, 'entities.py')

    @property
    def is_valid(self):
        return self._in_project

    @property
    def configuration(self):
        return self._configuration

    def _project_root(self):
        marker = self.marker
        for i in range(0, 5):
            if os.path.exists(marker) and os.path.isfile(marker):
                return os.path.dirname(os.path.realpath(marker))
            marker = os.path.join('..', marker)
        raise ValueError('Unable to determine project root.')

    def project_tree(self, path):
        with PushDir(path):
            root = self._project_root()

            tree = dict(
                    root=root,
                    src=None,
                    pkg=None,
                    resources=None,
                    transforms=None
            )

            for base, dirs, files in os.walk(root):
                if base.endswith('src'):
                    tree['src'] = base
                elif 'resources' in dirs:
                    tree['pkg'] = base
                elif base.endswith('resources'):
                    tree['resources'] = base
                elif base.endswith('transforms'):
                    tree['transforms'] = base
                    tree['common'] = os.path.join(base, 'common')

            return tree
