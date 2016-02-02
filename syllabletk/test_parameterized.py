# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import panphon
import _parameterized
import logging
import yaml

class TestPhonoRepr(unittest.TestCase):
    def setUp(self):
        self.ft = panphon.FeatureTable()

    def test_syllabify1(self):
        phonr = _parameterized.PhonoRepr(self.ft, 'pralstak')
        logging.debug('phonr.segs={}'.format(phonr.segs))
        phonr.marks = ['O', 'O', 'N', 'C', 'O', 'O', 'N', 'C']
        self.assertEqual(phonr.syllabified(), [(['p', 'r'], ['a'], ['l']), (['s', 't'], ['a'], ['k'])])


class TestPS1(unittest.TestCase):
    def setUp(self):
        self.ft = panphon.FeatureTable()
        with open('../tur.yml', 'r') as f:
            ons_cod = yaml.load(f.read())
            ons = ons_cod['initials'].keys()
            cod = ons_cod['finals'].keys()
        self.ps = _parameterized.ParameterizedSyllabifier((ons, cod))

    def test_syllabify1(self):
        self.assertEqual(self.ps.syllabify('pod'), (['p'], ['o'], ['d']))

    def test_syllabify2(self):
        self.assertEqual(self.ps.syllabify('jod'), (['j'], ['o'], ['d']))

if __name__ == '__main__':
    unittest.main()
