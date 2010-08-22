# -*- coding: utf-8 -*-

"""Test tagtools.py"""

from tagtools import FlickrTokenizer, DeliciousTokenizer, CommaTokenizer, \
                     TagWithSeparatorException
import unittest


class TagToolTestCase(unittest.TestCase):
    def _test(self, tagstr, expected):
        got = self.serializer.str2tags(tagstr)
        r = []
        for tag in got:
            if tag.is_machinetag:
                r.append((tag.clean, tag.raw, tag.namespace, tag.predicate,
                          tag.value))
            else:
                r.append((tag.clean, tag.raw))
        self.assertEqual(len(got), len(expected))
        for tag, exp in zip(got, expected):
            if len(exp) == 5:
                clean, raw, namespace, predicate, value = exp
                is_machine = True
            else:
                if len(exp) == 2:
                    clean, raw = exp
                else:
                    clean, raw = None, None
                namespace, predicate, value = None, None, None
                is_machine = False
            self.assertEqual(is_machine, tag.is_machinetag)
            self.assertEqual(clean, tag.clean)
            self.assertEqual(raw, tag.raw)
            self.assertEqual(namespace, tag.namespace)
            self.assertEqual(predicate, tag.predicate)
            self.assertEqual(value, tag.value)

class TestFlickrTokenizer(TagToolTestCase):

    def setUp(self):
        self.serializer = FlickrTokenizer

    def test_flickr_str2tags(self):
        test = self._test

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
        test(
          'tag1 tag2:foo tag3:bar=baz tag4:aa="a b c d" "  tag5:bb="e f g h',
          [('tag1', 'tag1'), ('tag2:foo', 'tag2:foo'),
           ('tag3:bar=baz', 'tag3:bar=baz', 'tag3', 'bar', 'baz'),
           ('tag4:aa=a b c d', 'tag4:aa=a b c d', 'tag4', 'aa', 'a b c d'),
           ('tag5:bb=e', 'tag5:bb=e', 'tag5', 'bb', 'e'),
           ('f', 'f'), ('g', 'g'), ('h', 'h')])


    def test_flickr_tags2str(self):
        def test(tags, expected):
            self.assertEqual(expected, FlickrTokenizer.tags2str(tags))
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


class TestDeliciousTokenizer(TagToolTestCase):

    def setUp(self):
        self.serializer = DeliciousTokenizer

    def test_delicious_str2tags(self):
        test = self._test
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
            self.assertEqual(expected, DeliciousTokenizer.tags2str(tags))
        test([], '')
        test(['t1'], 't1')
        test(['t1', 't2', 't3'], 't1 t2 t3')
        test(['t1', 't2', 't3'], 't1 t2 t3')
        self.assertRaises(TagWithSeparatorException,
            DeliciousTokenizer.tags2str, ['t 1'])


class TestCommaTokenizer(TagToolTestCase):

    def setUp(self):
        self.serializer = CommaTokenizer

    def test_comma_str2tags(self):
        test = self._test
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
            self.assertEqual(expected, CommaTokenizer.tags2str(tags))
        test([], '')
        test(['t1'], 't1')
        test(['t1', 't2', 't3'], 't1, t2, t3')
        test(['t  1', 't   2', 't 3'], 't  1, t   2, t 3')
        self.assertRaises(TagWithSeparatorException,
            CommaTokenizer.tags2str, ['t,1'])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
