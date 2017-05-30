from unittest import TestCase
from canari.maltego.transform import Transform
from canari.framework import *

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class TransformTests(TestCase):
    """
    TODO: Test cases for ExternalCommand decorator.
    """

    def get_transform_name(self, t):
        return '.'.join([t.__module__.split('.', 1)[0], t.__name__])

    def test_create_default_transform(self):
        class MyTransform(Transform):
            """This is a test."""
            pass
        transform = MyTransform()
        self.assertEqual(transform.name, self.get_transform_name(MyTransform))
        self.assertEqual(transform.display_name, 'My Transform')
        self.assertEqual(transform.author, '')
        self.assertEqual(transform.description, 'This is a test.')
        self.assertEqual(transform.help_url, '')
        self.assertFalse(transform.debug)
        self.assertFalse(transform.superuser)
        self.assertFalse(transform.deprecated)
        self.assertFalse(transform.remote)
        self.assertEqual(transform.transform_set, self.__module__.split('.', 1)[0].title())

    def test_create_default_superuser_transform(self):
        @RequireSuperUser
        class MyTransform(Transform):
            """This is a test."""
            pass
        transform = MyTransform()
        self.assertEqual(transform.name, self.get_transform_name(MyTransform))
        self.assertEqual(transform.display_name, 'My Transform')
        self.assertEqual(transform.author, '')
        self.assertEqual(transform.description, 'This is a test.')
        self.assertEqual(transform.help_url, '')
        self.assertFalse(transform.debug)
        self.assertTrue(transform.superuser)
        self.assertFalse(transform.deprecated)
        self.assertFalse(transform.remote)
        self.assertEqual(transform.transform_set, self.__module__.split('.', 1)[0].title())

    def test_create_default_superuser_debug_transform(self):
        @RequireSuperUser
        @EnableDebugWindow
        class MyTransform(Transform):
            """This is a test."""
            pass
        transform = MyTransform()
        self.assertEqual(transform.name, self.get_transform_name(MyTransform))
        self.assertEqual(transform.display_name, 'My Transform')
        self.assertEqual(transform.author, '')
        self.assertEqual(transform.description, 'This is a test.')
        self.assertEqual(transform.help_url, '')
        self.assertTrue(transform.debug)
        self.assertTrue(transform.superuser)
        self.assertFalse(transform.deprecated)
        self.assertFalse(transform.remote)
        self.assertEqual(transform.transform_set, self.__module__.split('.', 1)[0].title())

    def test_create_default_superuser_debug_remote_transform(self):
        @RequireSuperUser
        @EnableDebugWindow
        @EnableRemoteExecution
        class MyTransform(Transform):
            """This is a test."""
            pass
        transform = MyTransform()
        self.assertEqual(transform.name, self.get_transform_name(MyTransform))
        self.assertEqual(transform.display_name, 'My Transform')
        self.assertEqual(transform.author, '')
        self.assertEqual(transform.description, 'This is a test.')
        self.assertEqual(transform.help_url, '')
        self.assertTrue(transform.debug)
        self.assertTrue(transform.superuser)
        self.assertFalse(transform.deprecated)
        self.assertTrue(transform.remote)
        self.assertEqual(transform.transform_set, self.__module__.split('.', 1)[0].title())

    def test_create_default_superuser_debug_remote_deprecated_transform(self):
        @RequireSuperUser
        @EnableDebugWindow
        @EnableRemoteExecution
        @Deprecated
        class MyTransform(Transform):
            """This is a test."""
            pass
        transform = MyTransform()
        self.assertEqual(transform.name, self.get_transform_name(MyTransform))
        self.assertEqual(transform.display_name, 'My Transform')
        self.assertEqual(transform.author, '')
        self.assertEqual(transform.description, 'This is a test.')
        self.assertEqual(transform.help_url, '')
        self.assertTrue(transform.debug)
        self.assertTrue(transform.superuser)
        self.assertTrue(transform.deprecated)
        self.assertTrue(transform.remote)
        self.assertEqual(transform.transform_set, self.__module__.split('.', 1)[0].title())

    def test_create_no_description_transform(self):
        class MyTransform(Transform):
            pass
        transform = MyTransform()
        self.assertEqual(transform.name, self.get_transform_name(MyTransform))
        self.assertEqual(transform.display_name, 'My Transform')
        self.assertEqual(transform.author, '')
        self.assertEqual(transform.description, '')
        self.assertEqual(transform.help_url, '')
        self.assertFalse(transform.debug)
        self.assertFalse(transform.superuser)
        self.assertFalse(transform.deprecated)
        self.assertFalse(transform.remote)
        self.assertEqual(transform.transform_set, self.__module__.split('.', 1)[0].title())

    def test_create_explicit_name_transform(self):
        class MyTransform(Transform):
            name = 'foobar.Transform'
        transform = MyTransform()
        self.assertEqual(transform.name, 'foobar.Transform')
        self.assertEqual(transform.display_name, 'My Transform')
        self.assertEqual(transform.author, '')
        self.assertEqual(transform.description, '')
        self.assertEqual(transform.help_url, '')
        self.assertFalse(transform.debug)
        self.assertFalse(transform.superuser)
        self.assertFalse(transform.deprecated)
        self.assertFalse(transform.remote)
        self.assertEqual(transform.transform_set, self.__module__.split('.', 1)[0].title())

    def test_create_explicit_display_name_transform(self):
        class MyTransform(Transform):
            display_name = 'Foo'
        transform = MyTransform()
        self.assertEqual(transform.name, self.get_transform_name(MyTransform))
        self.assertEqual(transform.display_name, 'Foo')
        self.assertEqual(transform.author, '')
        self.assertEqual(transform.description, '')
        self.assertEqual(transform.help_url, '')
        self.assertFalse(transform.debug)
        self.assertFalse(transform.superuser)
        self.assertFalse(transform.deprecated)
        self.assertFalse(transform.remote)
        self.assertEqual(transform.transform_set, self.__module__.split('.', 1)[0].title())

    def test_create_explicit_description_transform(self):
        class MyTransform(Transform):
            description = 'foo'
        transform = MyTransform()
        self.assertEqual(transform.name, self.get_transform_name(MyTransform))
        self.assertEqual(transform.display_name, 'My Transform')
        self.assertEqual(transform.author, '')
        self.assertEqual(transform.description, 'foo')
        self.assertEqual(transform.help_url, '')
        self.assertFalse(transform.debug)
        self.assertFalse(transform.superuser)
        self.assertFalse(transform.deprecated)
        self.assertFalse(transform.remote)
        self.assertEqual(transform.transform_set, self.__module__.split('.', 1)[0].title())

    def test_create_explicit_help_url_transform(self):
        class MyTransform(Transform):
            help_url = 'foo'
        transform = MyTransform()
        self.assertEqual(transform.name, self.get_transform_name(MyTransform))
        self.assertEqual(transform.display_name, 'My Transform')
        self.assertEqual(transform.author, '')
        self.assertEqual(transform.description, '')
        self.assertEqual(transform.help_url, 'foo')
        self.assertFalse(transform.debug)
        self.assertFalse(transform.superuser)
        self.assertFalse(transform.deprecated)
        self.assertFalse(transform.remote)
        self.assertEqual(transform.transform_set, self.__module__.split('.', 1)[0].title())

    def test_create_explicit_author_transform(self):
        class MyTransform(Transform):
            author = 'foo'
        transform = MyTransform()
        self.assertEqual(transform.name, self.get_transform_name(MyTransform))
        self.assertEqual(transform.display_name, 'My Transform')
        self.assertEqual(transform.author, 'foo')
        self.assertEqual(transform.description, '')
        self.assertEqual(transform.help_url, '')
        self.assertFalse(transform.debug)
        self.assertFalse(transform.superuser)
        self.assertFalse(transform.deprecated)
        self.assertFalse(transform.remote)
        self.assertEqual(transform.transform_set, self.__module__.split('.', 1)[0].title())

    def test_create_explicit_transform_set(self):
        class MyTransform(Transform):
            transform_set = 'foo'
        transform = MyTransform()
        self.assertEqual(transform.name, self.get_transform_name(MyTransform))
        self.assertEqual(transform.display_name, 'My Transform')
        self.assertEqual(transform.author, '')
        self.assertEqual(transform.description, '')
        self.assertEqual(transform.help_url, '')
        self.assertFalse(transform.debug)
        self.assertFalse(transform.superuser)
        self.assertFalse(transform.deprecated)
        self.assertFalse(transform.remote)
        self.assertEqual(transform.transform_set, 'foo')