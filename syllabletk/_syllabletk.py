# -*- coding: utf-8 -*-

import panphon
import regex as re
from types import ListType


def count_true(items):
    """Return the number of elements in an iterable that evaluate as true."""
    return len([bool(x) for x in items if x])


class Syllabifier(object):
    """Syllabifies words of text.

    word -- Unicode IPA string
    """
    def __init__(self, word, son_peak=False):
        self.ft = panphon.FeatureTable()
        if son_peak:
            self.son_peak_parse(word)
        else:
            self.son_parse(word)

    def son_peak_parse(self, word):
        def is_peak(scores, i):
            score = scores[i]
            before = scores[i - 1]
            after = scores[i + 1]
            if score >= after and score >= before:
                return True
            else:
                return False
        word = list(panphon.segment_text(word))
        scores = map(lambda x: self.ft.sonority(x), word)
        scores = [0] + scores + [0]
        constits = len(word) * [' ']
        constits = ['<'] + constits + ['>']
        # Find nuclei
        for i in range(1, len(scores) - 1):
            if is_peak(scores, i):
                constits[i] = 'N'
        # Construct onsets.
        for i, con in enumerate(constits):
            if con == 'N':
                j = i
                while j > 0 \
                        and scores[j - 1] < scores[j] \
                        and constits[j - 1] == ' ':
                    j -= 1
                    constits[j] = 'O'
        # Construct codas.
        for i, con in enumerate(constits):
            if con == 'N':
                j = i
                while j < len(word) - 1 \
                        and scores[j] > scores[j + 1] \
                        and constits[j + 1] == ' ':
                    j += 1
                    constits[j] = 'C'
        # Leftover final Cs must be in coda.
        i = len(word) - 1
        while constits[i] == ' ' and i > 0:
            constits[i] = 'C'
            i -= 1
        # Finally, leftover Cs must be in onsets.
        for i, con in enumerate(constits):
            if con == ' ':
                constits[i] = 'O'
        self.word = word
        self.constituents = constits[1:-1]

    def son_parse(self, word):
        word = list(panphon.segment_text(word))
        scores = map(lambda x: self.ft.sonority(x), word)
        constituents = len(word) * [' ']
        assert type(scores) == ListType
        assert type(constituents) == ListType
        # Find nuclei.
        for i, score in enumerate(scores):
            if score >= 7:
                constituents[i] = 'N'
        # Construct onsets.
        for i, con in enumerate(constituents):
            if con == 'N':
                j = i
                while j > 0 \
                        and scores[j - 1] < scores[j] \
                        and constituents[j - 1] == ' ':
                    j -= 1
                    constituents[j] = 'O'
        # Construct codas.
        for i, con in enumerate(constituents):
            if con == 'N':
                j = i
                while j < len(word) - 1 \
                        and scores[j] > scores[j + 1] \
                        and constituents[j + 1] == ' ':
                    j += 1
                    constituents[j] = 'C'
        # Leftover final Cs must be in coda.
        i = len(word) - 1
        while constituents[i] == ' ' and i > 0:
            constituents[i] = 'C'
            i -= 1
        # Finally, leftover Cs must be in onsets.
        for i, con in enumerate(constituents):
            if con == ' ':
                constituents[i] = 'O'
        self.word = word
        self.constituents = constituents

    def as_tuples_iter(self):
        labels = ''.join(self.constituents)
        word = self.word
        for m in re.finditer(ur'(O*)(N)(C*)', labels):
            o, n, c = len(m.group(1)), len(m.group(2)), len(m.group(3))
            ons = ''.join(word[:o])
            nuc = ''.join(word[o:o + n])
            cod = ''.join(word[o + n:o + n + c])
            yield (ons, nuc, cod)
            word = word[o + n + c:]

    def as_tuples(self):
        return list(self.as_tuples_iter())

    def as_strings_iter(self):
        for (o, n, c) in self.as_tuples_iter():
            yield o + n + c

    def as_strings(self):
        return list(self.as_strings_iter())


class SyllableAnalyzer(object):
    """Provide rule-based analysis of the syllabic structure of a iterable
    stream of words.

    words -- an iterable of Unicode IPA strings.
    """
    def __init__(self):
        self.ft = panphon.FeatureTable()
        self.features = [
            # Language allows complex onsets
            ('SYL_ONS_COMPLEX',
             self.the_complex_onsets),

            # Language allows obstruent-approximant onsets
            ('SYL_ONS_OBS_APPROX',
             self.the_obstruent_approximant_onsets),

            # Language allows codas
            ('SYL_COD_SIMPLE',
             self.the_simple_codas),

            # Language allows complex codas
            ('SYL_COD_COMPLEX',
             self.the_complex_codas),

            # Language allows approximant-obstruent codas
            ('SYL_COD_APPROX_OBS',
             self.the_approximant_obstruent_codas),
        ]
        self.names, _ = zip(*self.features)
        self.values = {}  # dictionary of lists of floats

    def the_onsets(self, ws):
        onsets = []
        for w in ws:
            ons, _, _ = zip(*Syllabifier(w).as_tuples())
            onsets += ons
        return onsets

    def the_complex_onsets(self, ws):
        return map(lambda x: 1.0 if len(x) > 1 else 0.0,
                   self.the_onsets(ws))

    def the_obstruent_approximant_onsets(self, ws):
        regexp = self.ft.compile_regex_from_str(ur'[-syl -son -cons]' +
                                                ur'[-syl +son +cont]')
        return map(lambda x: 1.0 if regexp.match(x) else 0.0,
                   self.the_onsets(ws))

    def the_codas(self, ws):
        codas = []
        for w in ws:
            _, _, cod = zip(*Syllabifier(w).as_tuples())
            codas += cod
        return codas

    def the_simple_codas(self, ws):
        return map(lambda x: 1.0 if x else 0.0,
                   self.the_codas(ws))

    def the_complex_codas(self, ws):
        return map(lambda x: 1.0 if len(x) > 1 else 0.0,
                   self.the_codas(ws))

    def the_approximant_obstruent_codas(self, ws):
        regexp = self.ft.compile_regex_from_str(ur'[-syl +son +cont]' +
                                                ur'[-syl -son -cont]')
        return map(lambda x: 1.0 if regexp.match(x) else 0.0,
                   self.the_codas(ws))
