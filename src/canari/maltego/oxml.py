from safedexml import Model, fields

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'MaltegoElement',
    'fields'
]


class MaltegoElement(Model):
    """MaltegoElement is the base element for all XML elements defined in the Maltego DTD."""

    class meta:
        order_sensitive = False

    def __iadd__(self, other):
        return self

    def __add__(self, other):
        return self.__iadd__(other)