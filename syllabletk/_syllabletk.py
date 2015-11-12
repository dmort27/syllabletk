# -*- coding: utf-8 -*-

import panphon
import regex as re
from types import *

class Syllabifier(object):
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
            if score >= 4:
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

    def as_strings(self):
        for (o, n, c) in self.as_tuples_iter():
            yield o + n + c
