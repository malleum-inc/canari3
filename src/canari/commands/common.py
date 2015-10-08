from distutils.command.install import install
from distutils.dist import Distribution
from argparse import Action
from datetime import datetime
from importlib import import_module
from string import Template
import unicodedata
import subprocess
import sys
import os
import re

from pkg_resources import resource_filename

from canari.commands.framework import Command
from canari.config import CanariConfigParser


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class ParseFieldsAction(Action):
    """
    Custom argparse action to parse arguments for the run- and debug-transform commands. This ensures that all
    positional arguments are parsed and stored correctly.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        # Does the value argument have an equals ('=') sign that is not escaped and is the params argument populated?
        if namespace.params and re.search(r'(?<=[^\\])=', namespace.value):
            # if so, apply fix and pop last element of namespace.params into namespace.value
            # and copy what was in namespace.value into namespace.fields to fix everything
            values = namespace.value
            namespace.value = namespace.params.pop().replace('\=', '=')
            namespace.fields = values
            # Next parse our fields argument into a dictionary
            fields = re.split(r'(?<=[^\\])#', values)
            if fields:
                namespace.fields = dict(
                    map(
                        lambda x: [
                            field.replace('\#', '#').replace('\=', '=').replace('\\\\', '\\')
                            for field in re.split(r'(?<=[^\\])=', x, 1)
                        ],
                        fields
                    )
                )


@Command(description='Centralized Canari Management System')
def canari_main(opts):
    """
    This is the main function for the Canari commander. Nothing special here.
    """
    fix_pypath()
    opts.command_function(opts)


def get_bin_dir():
    """
    Returns the absolute path of the installation directory for the Canari scripts.
    """
    d = install(Distribution())
    d.finalize_options()
    return d.install_scripts


def to_utf8(s):
    return unicodedata.normalize('NFKD', unicode(s)).encode('ascii', 'ignore')


def sudo(args):
    p = subprocess.Popen([os.path.join(get_bin_dir(), 'pysudo')] + args)
    p.communicate()
    return p.returncode


def uproot():
    if os.name == 'posix' and not os.geteuid():
        login = os.getlogin()

        if login != 'root':
            print 'Why are you using root to run this command? You should be using %s! Bringing you down...' % login
            import pwd

            user = pwd.getpwnam(login)
            os.setgid(user.pw_gid)
            os.setuid(user.pw_uid)


def read_template(name, values):
    t = Template(file(resource_filename('canari.resources.template', '%s.plate' % name)).read())
    return t.substitute(**values)


def write_template(dst, data):
    print('creating file %s...' % dst)
    with file(dst, mode='wb') as w:
        w.write(data)


def generate_all(*args):
    return "\n\n__all__ = [\n    '%s'\n]" % "',\n    '".join(args)


def build_skeleton(*args):
    for d in args:
        if isinstance(d, list):
            d = os.sep.join(d)
        print('creating directory %s' % d)
        os.mkdir(d)


def fix_pypath():
    if '' not in sys.path:
        sys.path.insert(0, '')


def fix_binpath(paths):
    if paths is not None and paths:
        if isinstance(paths, basestring):
            os.environ['PATH'] = paths
        elif isinstance(paths, list):
            os.environ['PATH'] = os.pathsep.join(paths)


def load_object(classpath):
    package, cls = re.search(r'^(.*)\.([^\.]+)$', classpath).groups()
    module = import_module(package)
    return module.__dict__[cls]


def import_package(package):
    return __import__(package, globals(), locals(), ['*'])


def init_pkg():
    root = project_root()

    if root is not None:
        conf = os.path.join(root, '.canari')
        if os.path.exists(conf):
            c = CanariConfigParser()
            c.read(conf)
            return {
                'author': c['metadata/author'],
                'email': c['metadata/email'],
                'maintainer': c['metadata/maintainer'],
                'project': c['metadata/project'],
                'year': datetime.now().year
            }

    return {
        'author': '',
        'email': '',
        'maintainer': '',
        'project': '',
        'year': datetime.now().year
    }


def project_root():
    marker = '.canari'
    for i in range(0, 5):
        if os.path.exists(marker) and os.path.isfile(marker):
            return os.path.dirname(os.path.realpath(marker))
        marker = '..%s%s' % (os.sep, marker)
    raise ValueError('Unable to determine project root.')


def project_tree():
    root = project_root()

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

    return tree


def project_package_dir():
    working_dir = os.getcwd()
    try:
        working_dir = project_tree()['src']
    except ValueError:
        pass
    return working_dir


def parse_bool(question, default=True):
    choices = 'Y/n' if default else 'y/N'
    default = 'Y' if default else 'N'
    while True:
        ans = raw_input('%s [%s]: ' % (question, choices)).upper() or default
        if ans.startswith('Y'):
            return True
        elif ans.startswith('N'):
            return False
        else:
            print('Invalid selection (%s) must be either [y]es or [n]o.' % ans)


def parse_int(question, choices, default=0):
    while True:
        for i, c in enumerate(choices):
            print('[%d] - %s' % (i, c))
        ans = raw_input('%s [%d]: ' % (question, default)) or default
        try:
            ans = int(ans)
            if not 0 <= ans <= i:
                raise ValueError
            return ans
        except ValueError:
            print('Invalid selection (%s) must be an integer between 0 and %d.' % (ans, i))


def parse_str(question, default):
    return raw_input('%s [%s]: ' % (question, default)) or default


