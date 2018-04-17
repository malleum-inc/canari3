from __future__ import print_function

import sys

from canari.maltego.utils import highlight
from canari.pkgutils.transform import TransformDistribution
from canari.project import CanariProject
from canari.commands.common import canari_main
from canari.utils.fs import PushDir
from canari.commands.framework import SubCommand, Argument


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.6'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


# Argument parser
@SubCommand(
    canari_main,
    help="Lists transforms in a Canari package.",
    description="Lists transforms in a Canari package."
)
@Argument(
    'package',
    metavar='<package>',
    help='the name of the canari package to list transforms for.'
)
@Argument(
    '-w',
    '--working-dir',
    metavar='[working dir]',
    default=None,
    help="the path that will be used as the working directory for "
         "the canari package being listed (default: ~/.canari/)"
)
def list_transforms(opts):

    try:
        with PushDir(opts.working_dir or CanariProject().src_dir):
            transform_package = TransformDistribution(opts.package)
            for transform_class in transform_package.transforms:
                transform = transform_class()
                print('`- %s: %s' % (highlight(transform.name, 'green', True), transform.description), file=sys.stderr)
                print(highlight('  `- Maltego identifiers:', 'black', True), file=sys.stderr)
                print('    `- %s applies to %s in set %s' % (
                    highlight(transform.name, 'red', False),
                    highlight(transform.input_type._type_, 'red', False),
                    highlight(transform.transform_set, 'red', False)
                ), file=sys.stderr)
                print('', file=sys.stderr)
    except ValueError as e:
        print(e, file=sys.stderr)
        exit(-1)
