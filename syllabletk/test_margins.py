# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import unittest
import _margins
from collections import Counter


class TestMarginSniffer(unittest.TestCase):

    def setUp(self):
        self.ms = _margins.MarginSniffer(_margins.SonorityPeakSlicer)

    def test_margin_sniffer1(self):
        tokens = ['prak', 'strak', 'stri', 'aks', 'spj]
        self.ms.parse_tokens(tokens)
        expected_ini = Counter({'pr': 1, 'str': 2, '': 1, 'spj': 1})
        expected_fin = Counter({'k': 2, '': 2, 'ks': 1})
        self.assertDictEqual(dict(self.ms.initial), dict(expected_ini))
        self.assertDictEqual(dict(self.ms.final), dict(expected_fin))


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


class TestSonorityPeakSlicer(unittest.TestCase):

    def setUp(self):
        self.fss = _margins.SonorityPeakSlicer()

    def test_anom_fric_ons1(self):
        self.assertEqual(self.fss._adjust_anom_fric_ons([3, 1, 9]), [1, 1, 9])

    def test_anom_fric_ons2(self):
        self.assertEqual(self.fss._adjust_anom_fric_ons([3, 1, 9, 3, 1]), [1, 1, 9, 3, 1])

    def test_anom_fric_ons3(self):
        self.assertEqual(self.fss._adjust_anom_fric_ons([1, 3, 1, 9]), [1, 1, 1, 9])

    def test_anom_fric_cod1(self):
        self.assertEqual(self.fss._adjust_anom_fric_cod([8, 1, 3]), [8, 1, 1])

    def test_anom_fric_cod2(self):
        self.assertEqual(self.fss._adjust_anom_fric_cod([5, 9, 7, 1, 3, 1]), [5, 9, 7, 1, 1, 1])

    def test_initial1(self):
        self.assertEqual(self.fss._initial_onset([1, 1, 8, 8]), [1, 1])

    def test_initial2(self):
        self.assertEqual(self.fss._initial_onset([1, 1, 8, 8, 2]), [1, 1])

    def test_initial3(self):
        self.assertEqual(self.fss._initial_onset([1, 1, 6, 8, 1]), [1, 1, 6])

    def test_initial4(self):
        self.assertEqual(self.fss._initial_onset([1, 7]), [1])

    def test_initial5(self):
        self.assertEqual(self.fss._initial_onset([7]), [])

    def test_final1(self):
        self.assertEqual(self.fss._final_coda([8, 1]), [1])

    def test_final2(self):
        self.assertEqual(self.fss._final_coda([8, 1, 1]), [1, 1])

    def test_final3(self):
        self.assertEqual(self.fss._final_coda([1, 8, 1]), [1])

    def test_final4(self):
        self.assertEqual(self.fss._final_coda([7]), [])

    def test_parsing1(self):
        self.assertEqual(self.fss.parse('piklz'), ('p', 'z'))

    def test_parsing2(self):
        self.assertEqual(self.fss.parse('trambon'), ('tr', 'n'))

    def test_parsing3(self):
        self.assertEqual(self.fss.parse('snits'), ('sn', 'ts'))

    def test_parsing4(self):
        self.assertEqual(self.fss.parse('holtst'), ('h', 'ltst'))

    def test_parsing5(self):
        self.assertEqual(self.fss.parse('stits'), ('st', 'ts'))

    def test_parsing6(self):
        self.assertEqual(self.fss.parse('nawst'), ('n', 'st'))

    def test_parsing7(self):
        self.assertEqual(self.fss.parse('trenk'), ('tr', 'nk'))

    def test_parsing8(self):
        self.assertEqual(self.fss.parse('swist'), ('sw', 'st'))

    def test_parsing9(self):
        self.assertEqual(self.fss.parse('plizb'), ('pl', 'zb'))

    def test_parsing10(self):
        self.assertEqual(self.fss.parse('svensk'), ('sv', 'nsk'))

    def test_parsing11(self):
        self.assertEqual(self.fss.parse('strankl'), ('str', ''))

    def test_parsing12(self):
        self.assertEqual(self.fss.parse('test'), ('t', 'st'))

    def test_parsing13(self):
        self.assertEqual(self.fss.parse('sten'), ('st', 'n'))

    def test_parsing14(self):
        self.assertEqual(self.fss.parse('klp'), ('k', 'p'))

    def test_parsing14(self):
        self.assertEqual(self.fss.parse('b'), ('', ''))

    def test_parsing14(self):
        self.assertEqual(self.fss.parse('e'), ('', ''))


if __name__ == '__main__':
    unittest.main()
