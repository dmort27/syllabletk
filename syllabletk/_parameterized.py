# -*- coding: utf-8 -*-

import panphon

class ParameterizedSyllabifier(object):
    """Syllabifier that takes sniffed word-margin data as a parameter.

    margins - a 2-tuple of the form <init, fin> that provides attested onsets
    and codas to the syllabifier. Since these constituents are known to be
    possible onsets and codas, they are considered to be licit whenever they
    occur. When a sequence of consonants between nuclei cannot be divided into
    an onset from init and a coda from fin, sonority is used as a fallback.
    """

    def __init__(self, margins):
        self.attest_ons, self.attest_cod = margins
        self.attest_ons.sort(key=lambda x: len(x), reverse=True)
        self.attest_cod.sort(key=lambda x: len(x), reverse=True)
        self.ons_dict = {x: len(x) for x in self.attest_ons}
        self.cod_dict = {x: len(x) for x in self.attest_cod}
        self.ft = panphon.FeatureTable()

    def _mark_peaks_as_nuclei(self, scores, marks):
        """Mark the sonority peaks in a word as nuclei ('N'). THIS IS LIKELY
        INADEQUATE AND SHOULD BE REVISED.
        """
        nuclei = []
        for i in range(len(marks)):
            if i == 0:
                if scores[i] > scores[i + 1] and scores[i] >= 6:
                    marks[i] = 'N'
                    nuclei.append(i)
            elif i == len(marks) - 1:
                if scores[i] > scores[i - 1] and scores[i] >= 6:
                    marks[i] = 'N'
                    nuclei.append(i)
            else:
                if (scores[i] > scores[i - 1]) and \
                   (scores[i] > scores[i + 1]) and \
                   scores[i] >= 5:
                    marks[i] = 'N'
                    nuclei.append(i)
        return marks, nuclei

    def _mark_nuclei(self, segs, scores, marks):
        # Replaces _mark_peaks_as_nuclei
        #
        # Find longest onset in self.attest_ons
        # Mark next segment as nucleus
        # Try to match suffix with item in self._attest_cod
        # If not possible, find next sonority peak
        # Mark it, repeat.
        pass

    def _mark_glides(self, scores, marks, nuclei):
        """Mark glides following a nucleus as offglides (')'). The method
        does not handle rising-sonority diphthongs.
        """
        for i in nuclei:
            if i < len(marks) - 1:
                if marks[i + 1] == ' ' and scores[i + 1] >= 7:
                    marks[i + 1] = ')'
        return marks

    def _mark_ons_cod(self, scores, marks):
        pass

    def _ons_valid_by_son(self, scores):
        """Is onset valid according the the sonority sequencing principle?"""
        last_score = 0
        for score in scores:
            if score < last_score:
                return False
            last_score = score
        return True

    def _cod_valid_by_son(self, scores):
        """Is coda valid according the the sonority sequencing principle?"""
        last_score = 10
        for score in scores:
            if score > last_score:
                return False
            last_score = score
        return True

    def _clust_valid_by_son(self, scores):
        """If intervocalic cluster divides into licit coda and onset, return
        index dividing them, else None.
        """
        for i in range(len(scores) + 1):
            cod, ons = scores[:i], scores[i:]
            if self._ons_valid_by_son(ons) and self._cod_valid_by_son(cod):
                return cod, ons
        return None

    def _clust_valid_by_prec(self, segs):
        """If intervocalic cluster divides into licit coda and onset, by
        precedent, return index dividing them, else return None.
        """
        for i in range(len(segs) + 1):
            cod, ons = segs[:i], segs[i:]
            if ons in self.ons_dict and cod in self.cod_dict:
                return cod, ons
        return None

    def _mark_initial_onset(self, marks, nuclei):
        pass

    def _mark_final_coda(self, marks, nulcei):
        pass

    def parse(self, word):
        # Needs to be updated... badly.
        word = list(panphon.segment_text(word))  # Divide into segments.
        scores = map(lambda x: self.ft.sonority(x), word)  # Sonority scores.
        cons = len(scores) * [' ']
        cons, nuclei = self._mark_peaks_as_nuclei(scores, cons)
        cons = self._mark_glides(scores, cons, nuclei)
