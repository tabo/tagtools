# -*- coding: utf-8 -*-

"""Test tagtools.py"""

from tagtools import FlickrSerializer, DeliciousSerializer, CommaSerializer, \
                     TagWithSpaceException
import unittest


class TestFlickrSerializer(unittest.TestCase):

    def test_flickr_str2tags(self):
        def test(tagstr, expected):
            self.assertEqual(expected, FlickrSerializer.str2tags(tagstr))

        # I know these tests look weird, but I actually tried all of them
        # in flickr. This is how flickr does tagging.

        test(None, [])
        test('', [])
        test(' ', [])
        test('      ', [])
        test('t1', ['t1'])
        test('       t1', ['t1'])
        test('t1         ', ['t1'])
        test('t1 t2 t3', ['t1', 't2', 't3'])
        test('   t1    t2    t3   ', ['t1', 't2', 't3'])
        test('"t1"', ['t1'])
        test('   "t1"', ['t1'])
        test('"t1"   ', ['t1'])
        test('   "t1"   ', ['t1'])
        test('t1 "t2" t3', ['t1', 't2', 't3'])
        test('   "t1"   "t2"   "t3"  ', ['t1', 't2', 't3'])
        test('   t"1   t"2   t"3  ', ['t1   t2', 't3'])
        test('   ta"g1    "tag     number   2"    tag3    ',
             ['tag1    tag', 'number', '2', 'tag3'])
        test('   ta"g"1    "tag     number   2"    tag3    ',
             ['tag1', 'tag     number   2', 'tag3'])
        test('   t"a"g"1    "tag     number   2"    tag3    ',
             ['tag1    tag', 'number', '2', 'tag3'])
        test('   t"a"g"1    ""tag     number   2"    tag3    ',
             ['tag1    tag     number   2', 'tag3'])
        test('   ta"g"1    "ta"g     nu"mber   2"    tag3    ',
             ['tag1', 'tag', 'number   2', 'tag3'])
        test('   ta"g"1    "ta"g     nu"mber"   2"    tag3  "  ',
             ['tag1', 'tag', 'number', '2    tag3'])
        test(' "  t"a"""g"1    "ta"g     ""nu"mber"   2""""    tag3 " ""  ',
             ['tag1', 'tag', 'number', '2', 'tag3'])

    def test_flickr_tags2str(self):
        def test(tags, expected):
            self.assertEqual(expected, FlickrSerializer.tags2str(tags))
        test([], '')
        test(['t1'], 't1')
        test(['t1', 't2', 't3'], 't1 t2 t3')
        test(['t1   t2', 't3'], '"t1   t2" t3')
        test(['tag1    tag', 'number', '2', 'tag3'],
              '"tag1    tag" number 2 tag3')
        test(['tag1', 'tag     number   2', 'tag3'],
              'tag1 "tag     number   2" tag3')
        test(['tag1    tag', 'number', '2', 'tag3'],
              '"tag1    tag" number 2 tag3')
        test(['tag1    tag     number   2', 'tag3'],
              '"tag1    tag     number   2" tag3')
        test(['tag1', 'tag', 'number   2', 'tag3'],
              'tag1 tag "number   2" tag3')
        test(['tag1', 'tag', 'number', '2    tag3'],
              'tag1 tag number "2    tag3"')
        test(['tag1', 'tag', 'number', '2', 'tag3'],
              'tag1 tag number 2 tag3')


class TestDeliciousSerializer(unittest.TestCase):

    def test_delicious_str2tags(self):
        def test(tagstr, expected):
            self.assertEqual(expected, DeliciousSerializer.str2tags(tagstr))

        test(None, [])
        test('', [])
        test(' ', [])
        test('      ', [])
        test('t1', ['t1'])
        test('       t1', ['t1'])
        test('t1         ', ['t1'])
        test('t1 t2 t3', ['t1', 't2', 't3'])
        test('   t1    t2    t3   ', ['t1', 't2', 't3'])

    def test_delicious_tags2str(self):
        def test(tags, expected):
            self.assertEqual(expected, DeliciousSerializer.tags2str(tags))
        test([], '')
        test(['t1'], 't1')
        test(['t1', 't2', 't3'], 't1 t2 t3')
        test(['t1', 't2', 't3'], 't1 t2 t3')
        self.assertRaises(TagWithSpaceException,
            DeliciousSerializer.tags2str, ['t 1'])


class TestCommaSerializer(unittest.TestCase):
    def test_comma_str2tags(self):
        def test(tagstr, expected):
            self.assertEqual(expected, CommaSerializer.str2tags(tagstr))
        test(None, [])
        test('', [])
        test(',', [])
        test(',,,,,,', [])
        test('t1', ['t1'])
        test('  t   1   ', ['t   1'])
        test(',,,,,,,t1', ['t1'])
        test(',,,,,,, t  1 ', ['t  1'])
        test('t1,,,,,,,,,', ['t1'])
        test('t1,t2,t3', ['t1', 't2', 't3'])
        test(',,,t1,,,,t2,,,,t3,,,', ['t1', 't2', 't3'])
        test(',,,t   1,,,,t 2,,,,t    3,,,',
             ['t   1', 't 2', 't    3'])

    def test_comma_tags2str(self):
        def test(tags, expected):
            self.assertEqual(expected, CommaSerializer.tags2str(tags))
        test([], '')
        test(['t1'], 't1')
        test(['t1', 't2', 't3'], 't1, t2, t3')
        test(['t  1', 't   2', 't 3'], 't  1, t   2, t 3')


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
