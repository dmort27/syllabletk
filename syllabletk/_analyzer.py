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
             lambda syl: self.ft.match_pattern_seq(pat('[][]'), syl[0])),
            ('SYL_ONSET_COMPLEX_3',
             lambda syl: self.ft.match_pattern_seq(pat('[][][]'), syl[0])),
            ('SYL_ONSET_COMPLEX_4',
             lambda syl: self.ft.match_pattern_seq(pat('[][][][]'), syl[0])),
            ('SYL_ONSET_OBSTRUENT_OBSTRUENT',
             lambda syl: self.ft.match_pattern_seq(pat('[-son][-son]'), syl[0])),
            ('SYL_ONSET_PLOSIVE_PLOSIVE',
             lambda syl: self.ft.match_pattern_seq(pat('[-son -cont][-son -cont]'), syl[0])),
            ('SYL_ONSET_FRICATIVE_FRICATIVE',
             lambda syl: self.ft.match_pattern_seq(pat('[-son +cont][-son +cont]'), syl[0])),
            ('SYL_ONSET_PLOSIVE_FRICATIVE',
             lambda syl: self.ft.match_pattern_seq(pat('[-son -cont][-son +cont]'), syl[0])),
            ('SYL_ONSET_FRICATIVE_PLOSIVE',
             lambda syl: self.ft.match_pattern_seq(pat('[-son +cont][-son -cont]'), syl[0])),
            ('SYL_ONSET_FRICATIVE_PLOSIVE',
             lambda syl: self.ft.match_pattern_seq(pat('[-son +cont][-son -cont]'), syl[0])),
            ('SYL_ONSET_SONORANT_SONORANT',
             lambda syl: self.ft.match_pattern_seq(pat('[+son][+son]'), syl[0])),
            ('SYL_ONSET_SONORANT_GLIDE',
             lambda syl: self.ft.match_pattern_seq(pat('[+son][-syl -cons]'), syl[0])),
            ('SYL_ONSET_OBSTRUENT_SONORANT',
             lambda syl: self.ft.match_pattern_seq(pat('[+son][+son]'), syl[0])),
            ('SYL_ONSET_OBSTRUENT_GLIDE',
             lambda syl: self.ft.match_pattern_seq(pat('[-son][-syl -cons]'), syl[0])),
            ('SYL_ONSET_OBSTRUENT_LIQUID',
             lambda syl: self.ft.match_pattern_seq(pat('[-son][+cons +son -nas]'), syl[0])),
            ('SYL_ONSET_OBSTRUENT_NASAL',
             lambda syl: self.ft.match_pattern_seq(pat('[-son][+nas -syl]'), syl[0])),
            ('SYL_CODA_PLOSIVE',
             lambda syl: self.ft.match_pattern_seq(pat('[-son -cont]'), syl[2])),
            ('SYL_CODA_FRICATIVE',
             lambda syl: self.ft.match_pattern_seq(pat('[-son +cont]'), syl[2])),
            ('SYL_CODA_NASAL',
             lambda syl: self.ft.match_pattern_seq(pat('[-syl +son +nas]'), syl[2])),
            ('SYL_CODA_LIQUID',
             lambda syl: self.ft.match_pattern_seq(pat('[-syl +son -nas]'), syl[2])),
            ('SYL_CODA_COMPLEX_2',
             lambda syl: self.ft.match_pattern_seq(pat('[][]'), syl[2])),
            ('SYL_CODA_COMPLEX_3',
             lambda syl: self.ft.match_pattern_seq(pat('[][][]'), syl[2])),
            ('SYL_CODA_COMPLEX_4',
             lambda syl: self.ft.match_pattern_seq(pat('[][][][]'), syl[2])),
            ('SYL_CODA_OBSTRUENT_OBSTRUENT',
             lambda syl: self.ft.match_pattern_seq(pat('[-son][-son]'), syl[2])),
            ('SYL_CODA_PLOSIVE_PLOSIVE',
             lambda syl: self.ft.match_pattern_seq(pat('[-son -cont][-son -cont]'), syl[2])),
            ('SYL_CODA_FRICATIVE_FRICATIVE',
             lambda syl: self.ft.match_pattern_seq(pat('[-son -cont][-son -cont]'), syl[2])),
            ('SYL_CODA_PLOSIVE_FRICATIVE',
             lambda syl: self.ft.match_pattern_seq(pat('[-son -cont][-son +cont]'), syl[2])),
            ('SYL_CODA_FRICATIVE_PLOSIVE',
             lambda syl: self.ft.match_pattern_seq(pat('[-son +cont][-son -cont]'), syl[2])),
            ('SYL_CODA_SONORANT_SONORANT',
             lambda syl: self.ft.match_pattern_seq(pat('[+son][+son]'), syl[2])),
            ('SYL_CODA_LIQUID_NASAL',
             lambda syl: self.ft.match_pattern_seq(pat('[-syl +son -nas][-syl +son +nas]'), syl[2])),
            ('SYL_CODA_SONORANT_OBSTRUENT',
             lambda syl: self.ft.match_pattern_seq(pat('[+son][+son]'), syl[2])),
            ('SYL_NUCLEUS_BRANCHING',
             lambda syl: self.ft.match_pattern_seq(pat('[][]'), syl[1])),
        ]

    def analyze_syllable(self, syl):
        """Detect which structural patterns characterize a syllable.

        Iterates through the descriptions of phonotactic features and increments
        self.feature_counter by one for each feature whose structural
        description is matched.

        syl -- a 3-tuple <onset, nucleus, coda>, each part consisting of
        n-tuples of licit Unicode IPA strings.
        """
        self.syllable_counter += 1
        for name, f in self.features:
            if f(syl):
                self.feature_counter[name] += 1

    def analyze_syllables(self, syls):
        """Applies self.analyze_syllable to each syllable in a sequence.

        syls -- a sequence of syllables (see self.analyze_syllable).
        """
        for syl in syls:
            self.analyze_syllable(syl)
