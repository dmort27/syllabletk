# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import unittest
import _margins


class TestFixedSonoritySlicer(unittest.TestCase):

    def setUp(self):
        self.fss = _margins.FixedSonoritySlicer()

    def test_parsing1(self):
        self.assertEqual(self.fss.parse('sɪksθs'), ('s', 'ksθs'))

    def test_parsing2(self):
        self.assertEqual(self.fss.parse('stromboli'), ('str', ''))

    def test_parsing3(self):
        self.assertEqual(self.fss.parse('snɪtʃ'), ('sn', 'tʃ'))

    def test_parsing4(self):
        self.assertEqual(self.fss.parse('bɹæmbl'), ('bɹ', 'mbl'))

    def test_parsing5(self):
        self.assertEqual(self.fss.parse('adz'), ('', 'dz'))

    def test_parsing6(self):
        self.assertEqual(self.fss.parse('klobəʃɹ'), ('kl', 'ʃɹ'))

    def test_parsing7(self):
        self.assertEqual(self.fss.parse('trenk'), ('tr', 'nk'))

if __name__ == '__main__':
    unittest.main()
