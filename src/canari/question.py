import click

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2016, canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'

__all__ = [
    'prompt_menu'
]


def prompt_menu(question, choices, default=0, **kwargs):
    if len(choices) == 1:
        return 0
    return click.prompt(
        '{}\n{}'.format('\n'.join('[%d] - %s' % (i, c) for i, c in enumerate(choices)), question),
        default=default,
        type=click.IntRange(0, len(choices) - 1),
        **kwargs
    )
