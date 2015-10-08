from unittest import TestCase
from canari.framework import *
from canari.maltego.entities import *

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class FrameworkTests(TestCase):

    def create_transform_function(self, uuids, inputs, is_superuser=False, is_deprecated=False, **kwargs):
        if is_superuser:
            if is_deprecated:
                @deprecated
                @superuser
                @configure(
                    label='To Foo',
                    description='This is a test transform',
                    uuids=uuids,
                    inputs=inputs,
                    **kwargs
                )
                def dotransform(*args):
                    pass
                return dotransform
            else:
                @superuser
                @configure(
                    label='To Foo',
                    description='This is a test transform',
                    uuids=uuids,
                    inputs=inputs,
                    **kwargs
                )
                def dotransform(*args):
                    pass
                return dotransform
        elif is_deprecated:
            @deprecated
            @configure(
                label='To Foo',
                description='This is a test transform',
                uuids=uuids,
                inputs=inputs,
                **kwargs
            )
            def dotransform(*args):
                pass
            return dotransform
        @configure(
            label='To Foo',
            description='This is a test transform',
            uuids=uuids,
            inputs=inputs,
            **kwargs
        )
        def dotransform(*args):
            pass
        return dotransform

    def assertConfigure(self, f, uuids, input_sets, is_debug=False, is_superuser=False, is_deprecated=False):
        self.assertListEqual(uuids, f.uuids)
        self.assertListEqual(input_sets, f.inputs)
        self.assertEqual(is_debug, f.debug)
        if is_superuser:
            self.assertEqual(is_superuser, f.privileged)
        else:
            self.assertFalse(hasattr(f, 'privileged'))
        if is_deprecated:
            self.assertEqual(is_deprecated, f.deprecated)
        else:
            self.assertFalse(hasattr(f, 'deprecated'))
        self.assertEqual('This is a test transform', f.description)

    def test_create_dotransform_with_one_input(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ]
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ]
        )

    def test_create_privileged_dotransform_with_one_input(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            is_superuser=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            is_superuser=True
        )

    def test_create_deprecated_dotransform_with_one_input(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            is_deprecated=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            is_deprecated=True
        )

    def test_create_debugged_dotransform_with_one_input(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            debug=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            is_debug=True
        )

    def test_create_privileged_deprecated_dotransform_with_one_input(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            is_deprecated=True,
            is_superuser=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            is_deprecated=True,
            is_superuser=True
        )

    def test_create_debugged_deprecated_dotransform_with_one_input(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            debug=True,
            is_deprecated=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            is_debug=True,
            is_deprecated=True
        )

    def test_create_debugged_privileged_dotransform_with_one_input(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            debug=True,
            is_superuser=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            is_debug=True,
            is_superuser=True
        )

    def test_create_debugged_deprecated_privileged_dotransform_with_one_input(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            debug=True,
            is_deprecated=True,
            is_superuser=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo'
            ],
            [
                ('Input Set', Domain)
            ],
            is_debug=True,
            is_deprecated=True,
            is_superuser=True
        )

    def test_create_dotransform_with_two_inputs(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ]
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ]
        )

    def test_create_privileged_dotransform_with_two_inputs(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            is_superuser=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            is_superuser=True
        )

    def test_create_deprecated_dotransform_with_two_inputs(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            is_deprecated=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            is_deprecated=True
        )

    def test_create_debugged_dotransform_with_two_inputs(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            debug=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            is_debug=True
        )

    def test_create_privileged_deprecated_dotransform_with_two_input(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            is_deprecated=True,
            is_superuser=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            is_deprecated=True,
            is_superuser=True
        )

    def test_create_debugged_deprecated_dotransform_with_two_input(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            debug=True,
            is_deprecated=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            is_debug=True,
            is_deprecated=True
        )

    def test_create_debugged_privileged_dotransform_with_two_input(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            debug=True,
            is_superuser=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            is_debug=True,
            is_superuser=True
        )

    def test_create_debugged_deprecated_privileged_dotransform_with_two_input(self):
        f = self.create_transform_function(
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            debug=True,
            is_deprecated=True,
            is_superuser=True
        )
        self.assertConfigure(
            f,
            [
                'unittest.v2.BarToFoo_1'
                'unittest.v2.BarToFoo_2'
            ],
            [
                ('Input Set 1', Domain),
                ('Input Set 2', IPv4Address)
            ],
            is_debug=True,
            is_deprecated=True,
            is_superuser=True
        )