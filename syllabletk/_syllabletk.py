# -*- coding: utf-8 -*-

import panphon

class Syllabifier(object):
    def __init__(self):
        self.ft = FeatureTable()

    def son_parse(self, word):
        self.scores = map(lambda x: self.ft.sonority(x), word)
        self.constituents = len(word) * ' '
        # Find nuclei
        for i, score in enumerate(self.scores):
            if score >= 4:
                self.constituents[i] = 'N'
        # Construct onsets
        for i in range(word):
            if self.constituents[i] == 'N':
                j = i
                while j > 0 \
                        and self.scores[j-1] < self.scores[j] \
                        and self.constituents[j-i] == ' ':
                    j -= 1
                    self.constituents[j] == 'O'
        # Construct codas
        for i in range(word):
            if self.constituents[i] = 'N':
                j = i
                while j < len(word) - 2 \
                        and self.scores[j] > self.scores[j+1] \
                        and self.constituents[j+1] == ' ':
                    j += 1
                    self.constituents[j] == 'C'