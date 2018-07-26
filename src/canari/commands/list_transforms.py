import click

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.6'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'


def list_transforms(transform_package):
    click.secho('Canari Transforms:', fg='yellow', bold=True)
    for transform in transform_package.transforms:
        click.echo('`- %s: %s' % (click.style(transform.name, 'green', bold=True), transform.description))
        click.secho('  `- Maltego identifiers:', bold=True)
        click.echo('    `- %s applies to %s in set %s' % (
            click.style(transform.name, 'red', False),
            click.style(transform.input_type._type_, 'red', False),
            click.style(transform.transform_set, 'red', False)
        ))
