# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import panphon
import _parameterized
import logging


class TestPhonoRepr(unittest.TestCase):
    def setUp(self):
        self.ft = panphon.FeatureTable()

    def test_syllabify1(self):
        phonr = _parameterized.PhonoRepr(self.ft, 'pralstak')
        logging.debug('phonr.segs={}'.format(phonr.segs))
        phonr.marks = ['O', 'O', 'N', 'C', 'O', 'O', 'N', 'C']
        self.assertEqual(phonr.syllabified(), [(['p', 'r'], ['a'], ['l']), (['s', 't'], ['a'], ['k'])])


class TestParameterizedSyllabifier(unittest.TestCase):
    def setUp(self):
        ons = [(), ('s', 'p', 'r'), ('p', 'r'), ('r'), ('p'), ('s'), ('t'), ('s', 't'), ('k')]
        cod = [(), ('l'), ('l', 'k',), ('l', 's'), ('k'), ('s'), ('t')]
        self.ft = panphon.FeatureTable()
        self.ps = _parameterized.ParameterizedSyllabifier((ons, cod))

    def test_longest_ons_prefix1(self):
        phonr = _parameterized.PhonoRepr(self.ft, 'praspol')
        phonr = self.ps._longest_ons_prefix(phonr)
        self.assertEqual(''.join(phonr.marks), 'OON    ')

    def test_longest_ons_prefix2(self):
        phonr = _parameterized.PhonoRepr(self.ft, 'spraspol')
        phonr = self.ps._longest_ons_prefix(phonr)
        self.assertEqual(''.join(phonr.marks), 'OOON    ')

    def test_longest_cod_suffix1(self):
        phonr = _parameterized.PhonoRepr(self.ft, 'praspol')
        phonr = self.ps._longest_cod_suffix(phonr)
        self.assertEqual(''.join(phonr.marks), '     NC')

    def test_mark_rem_nuc1(self):
        phonr = _parameterized.PhonoRepr(self.ft, 'prasapol')
        self.assertEqual(''.join(phonr.marks), '        ')
        phonr = self.ps._longest_ons_prefix(phonr)
        self.assertEqual(''.join(phonr.marks), 'OON     ')
        phonr = self.ps._longest_cod_suffix(phonr)
        self.assertEqual(''.join(phonr.marks), 'OON   NC')
        phonr = self.ps._mark_rem_nuclei(phonr)
        self.assertEqual(''.join(phonr.marks), 'OON N NC')

    def test_mark_rem_nuc2(self):
        phonr = _parameterized.PhonoRepr(self.ft, 'prasrpol')
        self.assertEqual(''.join(phonr.marks), '        ')
        phonr = self.ps._longest_ons_prefix(phonr)
        self.assertEqual(''.join(phonr.marks), 'OON     ')
        phonr = self.ps._longest_cod_suffix(phonr)
        self.assertEqual(''.join(phonr.marks), 'OON   NC')
        phonr = self.ps._mark_rem_nuclei(phonr)
        self.assertEqual(''.join(phonr.marks), 'OON N NC')

    def test_mark_offglides1(self):
        phonr = _parameterized.PhonoRepr(self.ft, 'prajvet')
        phonr = self.ps._longest_ons_prefix(phonr)
        phonr = self.ps._longest_cod_suffix(phonr)
        phonr = self.ps._mark_offglides(phonr)
        phonr = self.ps._mark_rem_nuclei(phonr)
        self.assertEqual(''.join(phonr.marks), 'OONG NC')

    def test_mark_offglides2(self):
        phonr = _parameterized.PhonoRepr(self.ft, 'prowstatsrkol')
        self.assertEqual(''.join(phonr.marks), '             ')
        phonr = self.ps._longest_ons_prefix(phonr)
        self.assertEqual(''.join(phonr.marks), 'OON          ')
        phonr = self.ps._longest_cod_suffix(phonr)
        self.assertEqual(''.join(phonr.marks), 'OON        NC')
        phonr = self.ps._mark_rem_nuclei(phonr)
        self.assertEqual(''.join(phonr.marks), 'OON   N  N NC')
        phonr = self.ps._mark_offglides(phonr)
        self.assertEqual(''.join(phonr.marks), 'OONG  N  N NC')

    def test_mark_all1(self):
        phonr = _parameterized.PhonoRepr(self.ft, 'prowstatsrkol')
        self.assertEqual(''.join(phonr.marks), '             ')
        phonr = self.ps._longest_ons_prefix(phonr)
        self.assertEqual(''.join(phonr.marks), 'OON          ')
        phonr = self.ps._longest_cod_suffix(phonr)
        self.assertEqual(''.join(phonr.marks), 'OON        NC')
        phonr = self.ps._mark_rem_nuclei(phonr)
        self.assertEqual(''.join(phonr.marks), 'OON   N  N NC')
        phonr = self.ps._mark_offglides(phonr)
        self.assertEqual(''.join(phonr.marks), 'OONG  N  N NC')
        phonr = self.ps._mark_intervocalic_clusts(phonr)
        self.assertEqual(''.join(phonr.marks), 'OONGOONCONONC')
        syllabified = [(['p', 'r'], ['o', 'w'], []),
                       (['s', 't'], ['a'], ['t']),
                       (['s'], ['r'], []),
                       (['k'], ['o'], ['l'])]
        self.assertEqual(phonr.syllabified(), syllabified)

    def test_mark_all2(self):
        phonr = _parameterized.PhonoRepr(self.ft, 'asta')
        self.assertEqual(''.join(phonr.marks), '    ')
        phonr = self.ps._longest_ons_prefix(phonr)
        self.assertEqual(''.join(phonr.marks), 'N   ')
        phonr = self.ps._longest_cod_suffix(phonr)
        self.assertEqual(''.join(phonr.marks), 'N  N')
        phonr = self.ps._mark_rem_nuclei(phonr)
        self.assertEqual(''.join(phonr.marks), 'N  N')
        phonr = self.ps._mark_offglides(phonr)
        self.assertEqual(''.join(phonr.marks), 'N  N')
        phonr = self.ps._mark_intervocalic_clusts(phonr)
        self.assertEqual(''.join(phonr.marks), 'NOON')


if __name__ == '__main__':
    unittest.main()
