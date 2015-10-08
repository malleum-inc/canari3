#!/usr/bin/env python

from common import canari_main, project_tree
from framework import SubCommand, Argument

from os import path, unlink
from re import sub


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.3'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def parse_args(args):
    if args.transform_dir is None:
        args.transform_dir = project_tree()['transforms']
    if args.transform in ['common', 'common.py']:
        print "Error: 'common' is not a transform module. Cannot delete this module."
        exit(-1)
    return args


@SubCommand(
    canari_main,
    help='Deletes a transform in the specified directory and auto-updates __init__.py.',
    description='Deletes a transform in the specified directory and auto-updates __init__.py.'
)
@Argument(
    'transform',
    metavar='<transform name>',
    help='The name of the transform you wish to delete.'
)
@Argument(
    '-d',
    '--transform-dir',
    metavar='<dir>',
    help='The directory from which you wish to delete the transform.',
    default=None
)
def delete_transform(args):

    opts = parse_args(args)

    initf = path.join(opts.transform_dir, '__init__.py')
    transform = opts.transform
    transformf = path.join(opts.transform_dir, transform if transform.endswith('.py') else '%s.py' % transform)

    if not path.exists(initf):
        print ('Directory %r does not appear to be a python package directory... quitting!' % opts.transform_dir)
        exit(-1)
    if not path.exists(transformf):
        print ("Transform %r doesn't exists... quitting" % transformf)
        exit(-1)

    print ("deleting transform %r..." % transformf)
    unlink(transformf)

    print ('updating %s' % initf)
    init = file(initf).read()

    with file(initf, mode='wb') as w:
        w.write(
            sub(
                r'\s*%r,?' % transform,
                '',
                init
            )
        )

    print ('done!')
