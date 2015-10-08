#!/usr/bin/env python

from common import canari_main, project_tree
from framework import SubCommand, Argument

from os import path, rename
from re import sub


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.3'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def parse_args(args):
    if args.transform_dir is None:
        args.transform_dir = project_tree()['transforms']
    return args


@SubCommand(
    canari_main,
    help='Renames a transform in the specified directory and auto-updates __init__.py.',
    description='Renames a transform in the specified directory and auto-updates __init__.py.'
)
@Argument(
    'transform',
    metavar='<old transform name>',
    help='The name of the transform you wish to rename.'
)
@Argument(
    'new_transform',
    metavar='<new transform name>',
    help='The desired name of the transform.'
)
@Argument(
    '-d',
    '--transform-dir',
    metavar='<dir>',
    help='The directory from which you wish to rename the transform.',
    default=None
)
def rename_transform(args):

    opts = parse_args(args)

    initf = path.join(opts.transform_dir, '__init__.py')
    transform = opts.transform
    transformf = path.join(opts.transform_dir, transform if transform.endswith('.py') else '%s.py' % transform )
    dtransform = opts.new_transform
    dtransformf = path.join(opts.transform_dir, dtransform if dtransform.endswith('.py') else '%s.py' % dtransform )

    if not path.exists(initf):
        print('Directory %r does not appear to be a python package directory... quitting!' % opts.transform_dir)
        exit(-1)
    if not path.exists(transformf):
        print("Transform %r doesn't exists... quitting" % transformf)
        exit(-1)
    if path.exists(dtransformf):
        print("Cannot overwrite existing transform %r... quitting" % dtransformf)
        exit(-1)
    if dtransform == transform:
        print ("Nothing to do here... the new name is the same as the old one?")
        exit(-1)

    print('renaming transform %r to %r...' % (transformf, dtransformf))
    rename(transformf, dtransformf)

    print('updating %s' % initf)
    init = file(initf).read()

    with file(initf, mode='wb') as w:
        w.write(
            sub(
                repr(transform),
                repr(dtransform),
                init
            )
        )

    print ('done!')
