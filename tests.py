# -*- coding: utf-8 -*-

"""Test tagtools.py"""

from tagtools import FlickrSerializer, DeliciousSerializer, CommaSerializer, \
                     TagWithSeparatorException
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
        test('T1', [('t1', 'T1')])
        test('       T1', [('t1', 'T1')])
        test('T1         ', [('t1', 'T1')])
        test('T1 T2 T3',
             [('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3')])
        test('   T1    T2    T3   ',
             [('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3')])
        test('"T1"', [('t1', 'T1')])
        test('   "T1"', [('t1', 'T1')])
        test('"T1"   ', [('t1', 'T1')])
        test('   "T1"   ', [('t1', 'T1')])
        test('T1 "T2" T3', [('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3')])
        test('   "T1"   "T2"   "T3"  ',
             [('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3')])
        test('   T"1   T"2   T"3  ',
             [('t1   t2', 'T1   T2'), ('t3', 'T3')])
        test('   Ta"G1    "tAg     nUmber   2"    taG3    ',
             [('tag1    tag', 'TaG1    tAg'), ('number', 'nUmber'),
              ('2', '2'), ('tag3', 'taG3')])
        test('   Ta"G"1    "tAg     numbEr   2"    taG3    ',
             [('tag1', 'TaG1'), ('tag     number   2',
               'tAg     numbEr   2'), ('tag3', 'taG3')])
        test('   t"A"G"1    "tAg     nUMber   2"    tAG3    ',
             [('tag1    tag', 'tAG1    tAg'), ('number', 'nUMber'),
             ('2', '2'), ('tag3', 'tAG3')])
        test('   t"a"g"1    ""tag     number   2"    tag3    ',
             [('tag1    tag     number   2', 'tag1    tag     number   2'),
              ('tag3', 'tag3')])
        test('   ta"g"1    "ta"g     nu"mber   2"    tag3    ',
             [('tag1', 'tag1'), ('tag', 'tag'), ('number   2', 'number   2'),
              ('tag3', 'tag3')])
        test('   ta"g"1    "ta"g     nu"mber"   2"    tag3  "  ',
             [('tag1', 'tag1'), ('tag', 'tag'), ('number', 'number'),
              ('2    tag3', '2    tag3')])
        test(' "  t"a"""g"1    "ta"g     ""nu"mber"   2""""    tag3 " ""  ',
             [('tag1', 'tag1'), ('tag', 'tag'), ('number', 'number'),
              ('2', '2'), ('tag3', 'tag3')])
        test('TaG taG GAT tag gat', [('tag', 'TaG'), ('gat', 'GAT')])
        test('"TaG" taG GAT "tag" g"a"t', [('tag', 'TaG'), ('gat', 'GAT')])

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
        test('T1', [('t1', 'T1')])
        test('       T1', [('t1', 'T1')])
        test('T1         ', [('t1', 'T1')])
        test('T1 T2 T3', [('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3')])
        test('   T1    T2    T3   ',
             [('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3')])
        test('TaG taG GAT tag gat', [('tag', 'TaG'), ('gat', 'GAT')])

    def test_delicious_tags2str(self):
        def test(tags, expected):
            self.assertEqual(expected, DeliciousSerializer.tags2str(tags))
        test([], '')
        test(['t1'], 't1')
        test(['t1', 't2', 't3'], 't1 t2 t3')
        test(['t1', 't2', 't3'], 't1 t2 t3')
        self.assertRaises(TagWithSeparatorException,
            DeliciousSerializer.tags2str, ['t 1'])


class TestCommaSerializer(unittest.TestCase):
    def test_comma_str2tags(self):
        def test(tagstr, expected):
            self.assertEqual(expected, CommaSerializer.str2tags(tagstr))
        test(None, [])
        test('', [])
        test(',', [])
        test(',,,,,,', [])
        test('T1', [('t1', 'T1')])
        test('  T   1   ', [('t   1', 'T   1')])
        test(',,,,,,,T1', [('t1', 'T1')])
        test(',,,,,,, T  1 ', [('t  1', 'T  1')])
        test('T1,,,,,,,,,', [('t1', 'T1')])
        test('T1,T2,T3', [('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3')])
        test(',,,T1,,,,T2,,,,T3,,,',
             [('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3')])
        test(',,,T   1,,,,T 2,,,,T    3,,,',
             [('t   1', 'T   1'), ('t 2', 'T 2'), ('t    3', 'T    3')])
        test('TaG,taG,GAT,tag,gat', [('tag', 'TaG'), ('gat', 'GAT')])

    def test_comma_tags2str(self):
        def test(tags, expected):
            self.assertEqual(expected, CommaSerializer.tags2str(tags))
        test([], '')
        test(['t1'], 't1')
        test(['t1', 't2', 't3'], 't1, t2, t3')
        test(['t  1', 't   2', 't 3'], 't  1, t   2, t 3')
        self.assertRaises(TagWithSeparatorException,
            CommaSerializer.tags2str, ['t,1'])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
