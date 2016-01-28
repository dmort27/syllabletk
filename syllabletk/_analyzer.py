from __future__ import print_function
from __future__ import unicode_literals

from panphon import FeatureTable
from panphon import pat
from collections import Counter


class SyllableAnalyzer(object):
    """Makes and tracks analyses of syllables.

    Given a sequence of syllables structured as 3-tuples of constituents (onset,
    nucleus, coda), each consisting of n-tuples of segments, this class tracks
    whether syllables exemplify particular structural features.
    """

    def __init__(self):
        self.ft = FeatureTable()
        self.feature_counter = Counter()
        self.syllable_counter = 0
        self.features = [
            ('SYL_ONSET_COMPLEX_2',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[][]'), o)),
            ('SYL_ONSET_COMPLEX_3',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[][][]'), o)),
            ('SYL_ONSET_COMPLEX_4',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[][][][]'), o)),
            ('SYL_ONSET_OBSTRUENT_OBSTRUENT',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son][-son]'), o)),
            ('SYL_ONSET_PLOSIVE_PLOSIVE',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son -cont][-son -cont]'), o)),
            ('SYL_ONSET_FRICATIVE_FRICATIVE',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son +cont][-son +cont]'), o)),
            ('SYL_ONSET_PLOSIVE_FRICATIVE',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son -cont][-son +cont]'), o)),
            ('SYL_ONSET_FRICATIVE_PLOSIVE',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son +cont][-son -cont]'), o)),
            ('SYL_ONSET_FRICATIVE_PLOSIVE',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son +cont][-son -cont]'), o)),
            ('SYL_ONSET_SONORANT_SONORANT',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[+son][+son]'), o)),
            ('SYL_ONSET_SONORANT_GLIDE',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[+son][-syl -cons]'), o)),
            ('SYL_ONSET_OBSTRUENT_SONORANT',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[+son][+son]'), o)),
            ('SYL_ONSET_OBSTRUENT_GLIDE',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son][-syl -cons]'), o)),
            ('SYL_ONSET_OBSTRUENT_LIQUID',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son][+cons +son -nas]'), o)),
            ('SYL_ONSET_OBSTRUENT_NASAL',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son][+nas -syl]'), o)),
            ('SYL_CODA_PLOSIVE',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[-son -cont]'), c)),
            ('SYL_CODA_FRICATIVE',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[-son +cont]'), c)),
            ('SYL_CODA_NASAL',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[-syl +son +nas]'), c)),
            ('SYL_CODA_LIQUID',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[-syl +son -nas]'), c)),
            ('SYL_CODA_COMPLEX_2',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[][]'), c)),
            ('SYL_CODA_COMPLEX_3',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[][][]'), c)),
            ('SYL_CODA_COMPLEX_4',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[][][][]'), c)),
            ('SYL_CODA_OBSTRUENT_OBSTRUENT',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[-son][-son]'), c)),
            ('SYL_CODA_PLOSIVE_PLOSIVE',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[-son -cont][-son -cont]'), c)),
            ('SYL_CODA_FRICATIVE_FRICATIVE',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[-son -cont][-son -cont]'), c)),
            ('SYL_CODA_PLOSIVE_FRICATIVE',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[-son -cont][-son +cont]'), c)),
            ('SYL_CODA_FRICATIVE_PLOSIVE',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[-son +cont][-son -cont]'), c)),
            ('SYL_CODA_SONORANT_SONORANT',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[+son][+son]'), c)),
            ('SYL_CODA_LIQUID_NASAL',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[-syl +son -nas][-syl +son +nas]'), c)),
            ('SYL_CODA_SONORANT_OBSTRUENT',
             lambda (_, __, c): self.ft.match_pattern_seq(pat('[+son][+son]'), c)),
            ('SYL_NUCLEUS_BRANCHING',
             lambda (_, n, __): self.ft.match_pattern_seq(pat('[][]'), n)),
        ]

    def analyze_syllable(self, syl):
        self.syllable_counter += 1
        for name, f in self.features:
            if f(syl):
                self.feature_counter[name] += 1
