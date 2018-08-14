import zlib
from unittest import TestCase
from pkg_resources import resource_filename
from canari.utils.wordlist import wordlist


class WordListTests(TestCase):

    def test_simple_wordlist_resource(self):
        self.assertListEqual(
            ['1', '2', '3', '4', '5'],
            wordlist('file://%s' % resource_filename('tests.resources', 'wordlist.txt'))
        )

    def test_simple_wordlist_resource_ignore(self):
        self.assertListEqual(
            ['2', '3', '4', '5'],
            wordlist('file://%s' % resource_filename('tests.resources', 'wordlist.txt'), ignore='^1')
        )

    def test_simple_wordlist_resource_strip(self):
        self.assertListEqual(
            ['', '2', '3', '4', '5'],
            wordlist('file://%s' % resource_filename('tests.resources', 'wordlist.txt'), strip='^1')
        )

    def test_simple_wordlist_resource_gz(self):
        self.assertListEqual(
            ['', '3', '4', '5'],
            wordlist('file://%s' % resource_filename('tests.resources', 'wordlist.txt.gz'), strip='^1', ignore='^2')
        )

    def test_wordlist_object_return(self):
        self.assertEqual(1, wordlist(1))

    def test_wordlist_empty_string(self):
        self.assertEqual([], wordlist(''))

    def test_callable_match(self):
        self.assertEqual(
            ['1', '2', '3', '4', '5'],
            wordlist(
                'file://%s' % resource_filename('tests.resources', 'wordlist.txt'),
                match=lambda d: d.decode('utf8').split('\n')
            )
        )

    def test_callable_decompressor(self):
        self.assertEqual(
            ['1', '2', '3', '4', '5'],
            wordlist(
                'file://%s' % resource_filename('tests.resources', 'wordlist.txt.gz'),
                decompressor=lambda d: zlib.decompress(d, 16 + zlib.MAX_WBITS)
            )
        )
