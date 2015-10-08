from datetime import datetime
from getpass import getuser
from os import path

from mrbob.configurator import Configurator

from common import canari_main
from framework import SubCommand, Argument
import canari


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


@SubCommand(
    canari_main,
    help='Creates a Canari transform package skeleton.',
    description='Creates a Canari transform package skeleton.'
)
@Argument(
    'package',
    metavar='<package name>',
    help='The name of the canari package you wish to create.'
)
def create_package(opts):

    package_name = opts.package
    capitalized_package_name = package_name.capitalize()

    variables = {
        'project.name': package_name,
        'entity.example_name': 'My%sEntity' % capitalized_package_name,
        'entity.base_name': '%sEntity' % capitalized_package_name,
        'created.year': datetime.now().year,
        'canari.version': canari.__version__
    }

    defaults = {
        'project.create_example': True,
        'author.name': getuser()
    }

    if not path.exists(package_name):
        print('creating skeleton in %s' % package_name)
        configurator = Configurator('canari.resources.templates:create_package',
                                    package_name,
                                    {'non_interactive': False, 'remember_answers': True},
                                    variables=variables,
                                    defaults=defaults)
        configurator.ask_questions()
        configurator.render()
    else:
        print('A directory with the name %s already exists... exiting' % package_name)
        exit(-1)

    print('done!')