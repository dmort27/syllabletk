# -*- coding: utf-8 -*-

import panphon
# from _syllabletk import FailedParse
# from collections import Counter


class ParameterizedSyllabifier(object):

    def __init__(self, margins):
        self.attest_ons, self.attest_cod = margins
        self.ft = panphon.FeatureTable()

    def _mark_peaks_as_nuclei(self, scores, cons):
        # Mark the sonority peaks in a word as nuclei ('N').
        nuclei = []
        for i in range(len(cons)):
            if i == 0:
                if scores[i] > scores[i + 1] and scores[i] >= 6:
                    cons[i] = 'N'
                    nuclei.append(i)
            elif i == len(cons) - 1:
                if scores[i] > scores[i - 1] and scores[i] >= 6:
                    cons[i] = 'N'
                    nuclei.append(i)
            else:
                if (scores[i] > scores[i - 1]) and \
                   (scores[i] > scores[i + 1]) and \
                   scores[i] >= 5:
                    cons[i] = 'N'
                    nuclei.append(i)
        return cons, nuclei

    def _mark_glides(self, scores, cons, nuclei):
        # Mark glides following a nucleus as offglides (')'). The method
        # does not handle rising-sonority diphthongs.
        for i in nuclei:
            if i < len(cons) - 1:
                if cons[i + 1] == ' ' and scores[i + 1] >= 7:
                    cons[i + 1] = ')'
        return cons

    def _mark_ons_cod(self, scores, cons):
        pass

    def _mark_internal_clusters(self, scores, cons, word):

        def segs2str(segs):
            return ''.join(segs)

        def find_boundary(onset):
            return coda, onset

        st = 'INI'
        coda, onset = [], []
        for i, seg in enumerate(word):
            if st == 'INI':
                if cons[i] == 'N':
                    st == 'NUC'
                    onset, coda = [], []
                elif cons[i] == ' ':
                    cons[i] = 'O'
            elif st == 'NUC':
                if cons[i] in ['N', ')']:
                    pass
                elif cons == ' ':
                    st == 'INT'
                    onset.append(word[i])
            elif st == 'INT':
                if cons[i] == ' ':
                    onset.append(word[i])
                elif cons[i] == 'N':
                    j = find_boundary(i)
                    st = 'NUC'




    def _mark_initial_onset(self, cons, nuclei):
        pass

    def _mark_final_coda(self, cons, nulcei):
        pass

    def parse(self, word):
        word = list(panphon.segment_text(word))  # Divide into segments.
        scores = map(lambda x: self.ft.sonority(x), word)  # Sonority scores.
        cons = len(scores) * [' ']
        cons, nuclei = self._mark_peaks_as_nuclei(scores, cons)
        cons = self._mark_glides(scores, cons, nuclei)
