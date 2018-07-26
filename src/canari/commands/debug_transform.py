from canari.maltego.runner import local_transform_runner, console_writer
from canari.utils.fs import PushDir

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.7'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'


def debug_transform(transform, value, fields, params, project, config):
    with PushDir(project.src_dir):
        local_transform_runner(transform, value, fields, params, config, console_writer)
