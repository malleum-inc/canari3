from unittest import TestCase
from canari.framework import *
from canari.maltego.entities import *
from canari.maltego.transform import Transform

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class FrameworkTests(TestCase):

    def create_and_test_transform_function(self, is_superuser=False, is_deprecated=False, is_debug=False,
                                           is_remote=False, is_external=False, **kwargs):
        class TestTransform(Transform):
            pass

        for k, v in kwargs.iteritems():
            setattr(TestTransform, k, v)

        if is_superuser:
            RequireSuperUser(TestTransform)
        if is_deprecated:
            Deprecated(TestTransform)
        if is_debug:
            EnableDebugWindow(TestTransform)
        if is_remote:
            EnableRemoteExecution(TestTransform)
        # if is_external:
        #     ExternalCommand(TestTransform)

        return self.assertConfigure(TestTransform(), is_superuser, is_deprecated, is_debug, is_remote,
                                    is_external, **kwargs)

    def assertConfigure(self, transform, is_superuser=False, is_deprecated=False, is_debug=False, is_remote=False,
                        is_external=False, **kwargs):
        self.assertEqual(transform.superuser, is_superuser)
        self.assertEqual(transform.deprecated, is_deprecated)
        self.assertEqual(transform.debug, is_debug)
        self.assertEqual(transform.remote, is_remote)

    def test_deprecated_transform(self):
        self.create_and_test_transform_function(is_deprecated=True)

    def test_superuser_transform(self):
        self.create_and_test_transform_function(is_superuser=True)

    def test_debug_transform(self):
        self.create_and_test_transform_function(is_debug=True)

    def test_remote_transform(self):
        self.create_and_test_transform_function(is_remote=True)