#!/usr/bin/env python

import os
import re

from common import write_template, read_template, canari_main, init_pkg, project_tree
from framework import SubCommand, Argument

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.4'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def parse_args(args):
    if args.transform_dir is None:
        args.transform_dir = project_tree()['transforms']
    if args.transform in ['common', 'common.py']:
        print "Error: 'common' is a reserved module. Please name your transform something else."
        exit(-1)
    return args


@SubCommand(
    canari_main,
    help='Creates a new transform in the specified directory and auto-updates __init__.py.',
    description='Creates a new transform in the specified directory and auto-updates __init__.py.'
)
@Argument(
    'transform',
    metavar='<transform name>',
    help='The name of the transform you wish to duplicate.'
)
@Argument(
    'new_transform',
    metavar='<new transform name>',
    help='The name of the transform you wish to create.'
)
@Argument(
    '-d',
    '--transform-dir',
    metavar='<dir>',
    help='The directory in which you wish to create the transform.',
    default=None
)
def duplicate_transform(args):

    opts = parse_args(args)

    initf = os.path.join(opts.transform_dir, '__init__.py')
    transform = opts.transform[:-3] if opts.transform.endswith('.py') else opts.transform
    new_transform = opts.new_transform[:-3] if opts.new_transform.endswith('.py') else opts.new_transform

    if '.' in transform:
        print("Transform name (%r) cannot have a dot ('.')." % transform)
        exit(-1)
    elif not transform:
        print "You must specify a valid transform name."
        exit(-1)

    directory = opts.transform_dir
    transformf = os.path.join(directory, '%s.py' % transform)
    new_transformf = os.path.join(directory, '%s.py' % new_transform)

    if not os.path.exists(initf):
        print ('Directory %r does not appear to be a python package directory... quitting!' % opts.transform_dir)
        exit(-1)
    if os.path.exists(new_transformf):
        print ('Transform %r already exists... quitting' % new_transformf)
        exit(-1)

    print 'Copying transform %r to %r...' % (transformf, new_transformf)
    with open(new_transformf, 'wb') as dst:
        with open(transformf) as src:
            dst.write(src.read())

    print ('updating %s' % initf)
    init = file(initf).read()

    with file(initf, mode='wb') as w:
        w.write(
            re.sub(
                r'__all__\s*\=\s*\[',
                '__all__ = [\n    %r,' % new_transform,
                init
            )
        )

    print ('done!')