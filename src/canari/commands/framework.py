#!/usr/bin/env python

from argparse import ArgumentParser

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


__all__ = [
    'Command',
    'SubCommand',
    'Argument'
]


class Command(object):
    def __init__(self, *args, **kwargs):
        self.parser = ArgumentParser(*args, **kwargs)

    def __call__(self, func, *args, **kwargs):
        if hasattr(self.parser, 'parser_args'):
            for a, k in func.parser_args:
                self.parser.add_argument(*a, **k)

        def _func(args_=None, namespace=None):
            return func(self.parser.parse_args(args_, namespace))

        _func.parser = self.parser
        return _func


class SubCommand(object):
    def __init__(self, parent, *args, **kwargs):
        if not hasattr(parent, 'subparsers'):
            parent.subparsers = parent.parser.add_subparsers(
                title='subcommands',
                description='valid subcommands',
                help='additional help'
            )
        self.args = args
        self.kwargs = kwargs
        self.subparsers = parent.subparsers
        self.parser = None

    def __call__(self, func, *args, **kwargs):
        if not self.args:
            self.args = [func.__name__.replace('_', '-')]
        self.parser = self.subparsers.add_parser(*self.args, **self.kwargs)
        if hasattr(func, 'parser_args'):
            for a, k in func.parser_args:
                self.parser.add_argument(*a, **k)
        func.parser = self.parser
        func.parser.set_defaults(command_function=func)
        return func


class Argument(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func, *args, **kwargs):
        if not hasattr(func, 'parser_args'):
            func.parser_args = []
        func.parser_args.insert(0, (self.args, self.kwargs))
        return func