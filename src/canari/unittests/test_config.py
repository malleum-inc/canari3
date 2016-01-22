from unittest import TestCase
from canari.config import *
from pkg_resources import resource_filename
from canari.mode import set_canari_mode, CanariMode
import os

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'CanariConfigParserTest'
]


class CanariConfigParserTest(TestCase):
    def setUp(self):
        self.root_config_file = resource_filename('canari.unittests.resources', 'root.conf')
        self.canari_test_resource_dir = resource_filename('canari.unittests.resources', '')
        self.config_parser = load_config(self.root_config_file)
        self.path_environ = os.environ['PATH']
        os.environ['CANARI_TEST_RESOURCE_DIR'] = self.canari_test_resource_dir

    def create_config(self, name, content):
        config_parser = CanariConfigParser()
        for section, d in content.iteritems():
            config_parser.add_section(section)
            for option, value in d.iteritems():
                config_parser.set(section, option, value)
        config_parser.write(file(name, mode='w'))

    def test_load_config(self):
        self.assertIsInstance(self.config_parser, CanariConfigParser)

    def test_no_recurse_load(self):
        self.assertSetEqual(set(self.config_parser.sections()),
                             {'default', 'canari.local', 'canari.remote', 'types', 'types.dotted'})

    def test_recurse_load(self):
        # TODO: find a way of locating the sub conf file in unittests
        # self.config_parser = load_config(self.root_config_file, True)
        # self.assertSetEqual(set(self.config_parser.sections()),
        #                      {'default', 'canari.local', 'canari.remote', 'types', 'types.dotted', 'subconf'})
        pass

    def test_get_option_from_sub_config(self):
        # TODO: find a way of locating the sub conf file in unittests
        # self.config_parser = load_config(self.root_config_file, True)
        # self.assertEqual('hello world', self.config_parser['subconf.test'])
        pass

    def test_get_int_option(self):
        self.assertEqual(1, self.config_parser['types.int'])

    def test_get_float_option(self):
        self.assertEqual(1.0, self.config_parser['types.float'])

    def test_get_str_option(self):
        self.assertEqual('hello world', self.config_parser['types.str'])

    def test_get_str_escaped_comma_option(self):
        self.assertEqual('1,2,3', self.config_parser['types.str_escaped_comma'])

    def test_get_str_env_var_option(self):
        self.assertEqual(self.path_environ, self.config_parser['types.str_env_var'])

    def test_get_str_env_var_inline_option(self):
        self.assertEqual('foo%sbar' % self.path_environ, self.config_parser['types.str_env_var_inline'])

    def test_get_str_quotes_option(self):
        self.assertEqual("'hello'", self.config_parser['types.str_quotes'])

    def test_get_str_double_quotes_option(self):
        self.assertEqual('"hello"', self.config_parser['types.str_double_quotes'])

    def test_get_str_no_var_exists_option(self):
        self.assertEqual('$foo', self.config_parser['types.str_no_var_exists'])

    def test_get_callable_option(self):
        self.assertEqual('object://os/system', self.config_parser['types.callable'])

    def test_get_list_option(self):
        self.assertListEqual(self.config_parser['types.list'], [1, 2, 3])

    def test_get_list_with_escaped_commas_option(self):
        self.assertListEqual(self.config_parser['types.list_with_escaped_commas'], [1, '2,3'])

    def test_get_list_with_mixed_types_option(self):
        self.assertListEqual(self.config_parser['types.list_with_mixed_types'],
                             [1, 1.0, 'foo', 'foo,bar', self.path_environ])

    def test_get_option_with_dot_delimeter(self):
        self.assertEqual('foo%sbar' % self.path_environ, self.config_parser['types.str_env_var_inline'])

    def test_get_option_with_more_than_one_dot(self):
        self.assertEqual("'hello'", self.config_parser['types.dotted.var'])

    def test_get_wordlist_option(self):
        self.assertListEqual(self.config_parser['types.wordlist'], ['1', '2', '3', '4', '5'])

    def test_get_from_invalid_section(self):
        self.assertRaises(NoSectionError, self.config_parser.__getitem__, 'foo.bar')

    def test_get_invalid_option_from_valid_section(self):
        self.assertRaises(NoOptionError, self.config_parser.__getitem__, 'default.foo')

    def test_add_section(self):
        self.config_parser += 'test'
        self.assertTrue('test' in self.config_parser.sections())
        self.assertTrue('test' in self.config_parser)
        self.config_parser.add_section('test2')
        self.assertTrue('test2' in self.config_parser.sections())
        self.assertTrue('test2' in self.config_parser)

    def test_add_section_and_option(self):
        self.config_parser['test.test'] = 1
        self.assertTrue('test' in self.config_parser and 'test.test' in self.config_parser)

    def set_option(self, value, expected_value=None, expected_backend_value=None):
        self.config_parser['test.test'] = value
        if isinstance(value, list):
            self.assertListEqual(expected_value or value, self.config_parser['test.test'])
        else:
            self.assertEqual(expected_value or value, self.config_parser['test.test'])
        self.assertEqual(expected_backend_value or expected_value or str(value),
                         self.config_parser.get('test', 'test'))

    def test_set_int_option(self):
        self.set_option(1)

    def test_set_float_option(self):
        self.set_option(0.5)

    def test_set_str_option(self):
        self.set_option('hello world')

    def test_set_str_env_var_option(self):
        self.set_option('${PATH}', self.path_environ)

    def test_set_str_env_var_innline_option(self):
        self.set_option('foo${PATH}bar', 'foo%sbar' % self.path_environ)

    def test_set_str_quotes_option(self):
        self.set_option("'hello'")

    def test_set_str_double_quotes_option(self):
        self.set_option('"hello"')

    def test_set_callable_option(self):
        def set_callable():
            self.set_option(os.system, expected_value='object://posix/system',
                            expected_backend_value='object://posix/system')
        self.assertRaises(ValueError, set_callable)

    def test_set_list_option(self):
        self.set_option([1, 2, 3], expected_backend_value='1,2,3')

    def test_set_list_with_escaped_comma_option(self):
        self.set_option([1, '2,3'], expected_backend_value='1,2\\,3')

    def test_set_list_with_mixed_types_option(self):
        self.set_option([1, 1.0, 'foo', 'foo,bar', '${PATH}'],
                        [1, 1.0, 'foo', 'foo,bar', self.path_environ],
                        '1,1.0,foo,foo\,bar,%s' % self.path_environ)

    def test_set_dotted_var_option(self):
        self.config_parser['test.test.test'] = 1
        self.assertEqual(1, self.config_parser['test.test.test'])
        self.assertEqual('1', self.config_parser.get('test.test', 'test'))

    def test_set_unknown_type_option(self):
        self.set_option({'a': 1}, str({'a': 1}))

    def test_write_config(self):
        with file('foo.conf', 'w') as f:
            self.config_parser.write(f)
        self.assertTrue(os.path.exists('foo.conf'))
        c = CanariConfigParser()
        c.read('foo.conf')
        self.assertListEqual(c.sections(), self.config_parser.sections())
        self.assertDictEqual(c._sections, self.config_parser._sections)
        os.unlink('foo.conf')

    def test_merge_config(self):
        c = CanariConfigParser()
        c['test.test'] = 1
        self.config_parser.update(c)
        self.assertTrue(self.config_parser.has_section('test'))
        self.assertTrue(self.config_parser.has_option('test', 'test'))
        self.assertEqual(1, self.config_parser['test.test'])

    def test_fail_merge_config(self):
        self.assertRaises(ValueError, self.config_parser.update, dict(d=1))

    def test_delete_option(self):
        del self.config_parser['default/paths']
        self.assertTrue('default' in self.config_parser)
        self.assertFalse('default/paths' in self.config_parser)

    def test_delete_section(self):
        del self.config_parser['default']
        self.assertFalse('default' in self.config_parser)

