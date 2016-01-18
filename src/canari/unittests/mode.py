from unittest import TestCase
from canari.mode import *
import sys

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class ModeTests(TestCase):
    
    def setUp(self):
        self.tests = dict(
            is_remote_exec_mode=is_remote_exec_mode,
            is_plume_exec_mode=is_plume_exec_mode,
            is_local_exec_mode=is_local_exec_mode,
            is_debug_exec_mode=is_debug_exec_mode,
            is_dispatch_exec_mode=is_dispatch_exec_mode,
            is_unknown_exec_mode=is_unknown_exec_mode,
            is_local_debug_exec_mode=is_local_debug_exec_mode,
            is_local_dispatch_exec_mode=is_local_dispatch_exec_mode,
            is_local_unknown_exec_mode=is_local_unknown_exec_mode,
            is_remote_plume_debug_exec_mode=is_remote_plume_debug_exec_mode,
            is_remote_plume_dispatch_exec_mode=is_remote_plume_dispatch_exec_mode,
            is_remote_unknown_exec_mode=is_remote_unknown_exec_mode,
        )

    def test_initial_load(self):
        self.assertEqual(CanariMode.Unknown, get_canari_mode())
        
    def set_canari_mode(self, mode, truth_table):
        set_canari_mode(mode)
        self.assertEqual(mode, get_canari_mode())
        for name, func in self.tests.iteritems():
            expected_result = truth_table.issuperset([name])
            self.assertEqual(
                expected_result, bool(func()),
                '%s returned %s instead of %s (expected).' % (name, not expected_result, expected_result)
            )

    def test_set_remote_exec_mode(self):
        self.set_canari_mode(
            CanariMode.Remote,
            {'is_remote_exec_mode'}
        )

    def test_set_plume_exec_mode(self):
        self.set_canari_mode(
            CanariMode.Plume,
            {'is_plume_exec_mode'}
        )

    def test_set_local_exec_mode(self):
        self.set_canari_mode(
            CanariMode.Local,
            {'is_local_exec_mode'}
        )

    def test_set_debug_exec_mode(self):
        self.set_canari_mode(
            CanariMode.Debug,
            {'is_debug_exec_mode'}
        )

    def test_set_dispatch_exec_mode(self):
        self.set_canari_mode(
            CanariMode.Dispatch,
            {'is_dispatch_exec_mode'}
        )

    def test_set_unknown_exec_mode(self):
        self.set_canari_mode(
            CanariMode.Unknown,
            {'is_unknown_exec_mode'}
        )

    def test_set_local_debug_exec_mode(self):
        self.set_canari_mode(
            CanariMode.LocalDebug,
            {'is_debug_exec_mode', 'is_local_exec_mode', 'is_local_debug_exec_mode'}
        )

    def test_set_local_dispatch_exec_mode(self):
        self.set_canari_mode(
            CanariMode.LocalDispatch,
            {'is_dispatch_exec_mode', 'is_local_exec_mode', 'is_local_dispatch_exec_mode'}
        )

    def test_set_local_unknown_exec_mode(self):
        self.set_canari_mode(
            CanariMode.LocalUnknown,
            {'is_unknown_exec_mode', 'is_local_exec_mode', 'is_local_unknown_exec_mode'}
        )

    def test_set_remote_plume_debug_exec_mode(self):
        self.set_canari_mode(
            CanariMode.RemotePlumeDebug,
            {'is_plume_exec_mode', 'is_remote_exec_mode',
             'is_debug_exec_mode', 'is_remote_plume_debug_exec_mode'}
        )

    def test_set_remote_plume_dispatch_exec_mode(self):
        self.set_canari_mode(
            CanariMode.RemotePlumeDispatch,
            {'is_plume_exec_mode', 'is_remote_exec_mode',
             'is_dispatch_exec_mode', 'is_remote_plume_dispatch_exec_mode'}
        )

    def test_set_remote_unknown_exec_mode(self):
        self.set_canari_mode(
            CanariMode.RemoteUnknown,
            {'is_remote_exec_mode', 'is_unknown_exec_mode', 'is_remote_unknown_exec_mode'}
        )

    def tearDown(self):
        sys.modules.pop('canari.config', None)