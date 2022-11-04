# -*- coding: utf-8 -*-

import unittest
import _syllabletk


class TestSyllabifier(unittest.TestCase):
    def test_one_syllable(self):
        self.assertEqual(_syllabletk.Syllabifier(
                         hwelp', son_peak=True).as_tuples(),
                         [(hw', e', lp')])

    def test_more_complex_syllabification(self):
        self.assertEqual(_syllabletk.Syllabifier(
                         atrɐms', son_peak=True).as_tuples(),
                         [(', a', '), (tr', ɐ', ms')])

    def test_pterodactyl_syllabification(self):
        self.assertEqual(_syllabletk.Syllabifier(
                         ptɛrodaktyl', son_peak=True).as_tuples(),
                         [(pt', ɛ', '), (r', o', '),
                          (d', a', k'), (t', y', l')])

    def test_german_fricative_syllabification(self):
        self.assertEqual(_syllabletk.Syllabifier(
                         ʃveʁɪxkajt', son_peak=True).as_tuples(),
                         [(ʃv', e', '), (ʁ', ɪ', x'),
                          (k', aj', t')])

    def test_english_phonetic_syllabification(self):
        self.assertEqual(_syllabletk.Syllabifier(
                         painsalow', son_peak=True).as_tuples(),
                         [(p', ai', n'), (s', a', '),
                          (l', ow', ')])

    def test_diphthong_syllabification(self):
        self.assertEqual(_syllabletk.Syllabifier(
                         ʃɑɪnʃajn', son_peak=True).as_tuples(),
                         [(ʃ', ɑɪ', n'), (ʃ', aj', n')])


# Deprecated due to deprecation of _syllabletk.SyllableAnalyzerDepr.

class TestSyllableTK(unittest.TestCase):
    def setUp(self):
        self.sa = _syllabletk.SyllableAnalyzerDepr()

    def test_the_onsets(self):
        ws = [trup', pɹum', ap', strupon']
        results = [tr', pɹ', ', str', p']
        self.assertEqual(self.sa.the_onsets(ws), results)

    def test_the_codas(self):
        ws = [hwelp', pewl', pa', plawd', taptap']
        results = [lp', l', ', d', p', p']
        self.assertEqual(self.sa.the_codas(ws), results)

    def test_the_obstruent_sonorant_onsets(self):
        ws = [smaks', tliŋ', stap']
        results = [1.0, 1.0, 0.0]
        self.assertEqual(self.sa.the_obstruent_sonorant_onsets(ws),
                         results)

    def test_the_plosive_sonorant_onsets(self):
        ws = [pwak', snasplam', kap']
        results = [1.0, 0.0, 1.0, 0.0]
        self.assertEqual(self.sa.the_plosive_sonorant_onsets(ws),
                         results)

    def test_the_obstruent_approximant_onsets(self):
        ws = [tsup', pɹum', klap']
        results = [0.0, 1.0, 1.0]
        self.assertEqual(self.sa.the_obstruent_approximant_onsets(ws),
                         results)

    def test_the_plosive_approximant_onsets(self):
        ws = [tlup', pɹum', kwap', mleɡ']
        results = [1.0, 1.0, 1.0, 0.0]
        self.assertEqual(self.sa.the_plosive_approximant_onsets(ws),
                         results)

    def test_the_obstruent_obstruent_onsets(self):
        ws = [skup', ptum', kwap', mleɡ']
        results = [1.0, 1.0, 0.0, 0.0]
        self.assertEqual(self.sa.the_obstruent_obstruent_onsets(ws),
                         results)

    def test_the_plosive_plosive_onsets(self):
        ws = [ptuk', pɹum', kwap', ɡbo']
        results = [1.0, 0.0, 0.0, 1.0]
        self.assertEqual(self.sa.the_plosive_plosive_onsets(ws),
                         results)

    def test_the_sonorant_sonorant_onsets(self):
        ws = [mloŋ', mnemonik']
        results = [1.0, 1.0, 0.0, 0.0]
        self.assertEqual(self.sa.the_sonorant_sonorant_onsets(ws),
                         results)

    def test_the_nasal_nasal_onsets(self):
        ws = [mloŋ', mnemonik']
        results = [0.0, 1.0, 0.0, 0.0]
        self.assertEqual(self.sa.the_nasal_nasal_onsets(ws),
                         results)

    def test_the_complex_onsets(self):
        ws = [trup', pɹum', ap', strupon']
        results = [1.0, 1.0, 0.0, 1.0, 0.0]
        self.assertEqual(self.sa.the_complex_onsets(ws), results)

    def test_the_complex_onsets_2(self):
        ws = [trup', pɹum', ap', strupon']
        results = [1.0, 1.0, 0.0, 0.0, 0.0]
        self.assertEqual(self.sa.the_complex_onsets_2(ws), results)

    def test_the_complex_onsets_3(self):
        ws = [trup', spɹum', ap', strupon']
        results = [0.0, 1.0, 0.0, 1.0, 0.0]
        self.assertEqual(self.sa.the_complex_onsets_3(ws), results)

    def test_the_complex_onsets_4_or_more(self):
        ws = [trup', pɹum', ntsjap', pzlwustplon']
        results = [0.0, 0.0, 1.0, 1.0, 0.0]
        self.assertEqual(self.sa.the_complex_onsets_4_or_more(ws), results)

    def test_the_simple_codas(self):
        ws = [ka', rysp', ʃpil']
        results = [0.0, 0.0, 1.0]
        self.assertEqual(self.sa.the_simple_codas(ws), results)

    def test_the_complex_codas(self):
        ws = [ka', rysp', ʃpil']
        results = [0.0, 1.0, 0.0]
        self.assertEqual(self.sa.the_complex_codas(ws), results)

    def test_the_approximant_obstruent_codas(self):
        ws = [hwelp', pewl', 'paw', 'plawd']
        results = [1.0, 0.0, 0.0, 0.0]
        self.assertEqual(self.sa.the_approximant_obstruent_codas(ws),
                         results)

if __name__ == '__main__':
    unittest.main()
