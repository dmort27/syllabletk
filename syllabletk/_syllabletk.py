# -*- coding: utf-8 -*-

import panphon
import itertools
import regex as re
from types import *

class Syllabifier(object):
    """Syllabifies words of text.

    word -- Unicode IPA string
    """
    def __init__(self, word):
        self.ft = panphon.FeatureTable()
        self.son_parse(word)

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
                        and scores[j-1] < scores[j] \
                        and constituents[j-1] == ' ':
                    j -= 1
                    constituents[j] = 'O'
        # Construct codas.
        for i, con in enumerate(constituents):
            if con == 'N':
                j = i
                while j < len(word) - 1 \
                        and scores[j] > scores[j+1] \
                        and constituents[j+1] == ' ':
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
            nuc = ''.join(word[o:o+n])
            cod = ''.join(word[o+n:o+n+c])
            yield (ons, nuc, cod)
            word = word[o+n+c:]

    def as_tuples(self):
        return list(self.as_tuples_iter())

    def as_strings_iter(self):
        for (o, n, c) in self.as_tuples_iter():
            yield o + n + c

    def as_strings(self):
        return list(self.as_strings_iter())


class SyllableAnalyzer(object):
    """Provide rule-based analysis of the syllabic structure of a iterable stream of words.

    words -- an iterable of Unicode IPA strings.
    """
    def __init__(self):
        self.features = [

            # Language allows codas
            ('PHONOT_CODAS',
             self.has_codas),

            # Language allows complex codas
            ('PHONOT_CODAS_COMPLEX',
             self.has_complex_codas),

            # Language allows complex onsets
            ('PHONOT_ONSETS_COMPLEX',
             self.has_complex_onsets),
        ]
        self.names, _ = zip(*self.features)
        self.values = {} # dictionary of lists of floats

    def analyze(self, code, words):
        def to_float(x):
            return float(bool(x))
        values = []
        for _, func in self.features:
            value = to_float(func(words))
            values.append(value)
        self.values[code] = values

    def has_codas(self, ws):
        codas = []
        for w in ws:
            _, _, cod = zip(*Syllabifier(w).as_tuples())
            codas += cod
        return any(codas)

    def has_complex_codas(self, ws):
        codas = []
        for w in ws:
            _, _, cod = zip(*Syllabifier(w).as_tuples())
            codas += cod
        return any([c for c in codas if len(c) > 1])

    def has_complex_onsets(self, ws):
        onsets = []
        for w in ws:
            ons, _, _ = zip(*Syllabifier(w).as_tuples())
            onsets += ons
        return any([o for o in onsets if len(o) > 1])