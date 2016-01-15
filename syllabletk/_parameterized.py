# -*- coding: utf-8 -*-

import panphon
from collections import Counter
import datrie
# from _syllabletk import FailedParse
# from collections import Counter


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
        # May not be needed. Delete if not used.
        self.ons_trie = self._build_trie(self.attest_ons_rev)
        # Build trie of unreversed codas to find prefixes of consonant clusters.
        self.cod_trie = self._build_trie(self.attest_cod)
        self.ft = panphon.FeatureTable()

    def _build_trie(self, keys):
        trie = datrie.Trie(self._all_chars(keys))
        for key in keys:
            trie[key] = len(key)
        return trie

    def _all_chars(self, strings):
        """Return all unicode characters in a list of strings."""
        chars = Counter()
        for string in strings:
            for char in string:
                chars[char] += 1
        return ''.join(chars.keys())

    def _parse_cluster_attested(self, cluster):
        i = len(cluster)
        while i > 0:
            if cluster[:i] in self.cod_trie and cluster[i:] in self.ons_trie:
                return i
            i -= 1
        return None


    def _mark_peaks_as_nuclei(self, scores, marks):
        """Mark the sonority peaks in a word as nuclei ('N'). THIS MAY BE
        INADEQUATE.
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
            ons, cod = scores[:i], scores[i:]
            if self._ons_valid_by_son(ons) and self._cod_valid_by_son(cod):
                return i
        return None

    def _clust_valid_by_prec(self, segs):
        """If intervocalic cluster divides into licit coda and onset, by
        precedent, return index dividing them, else return None.
        """
        for i in range(len(segs) + 1):
            ons, cod = segs[:i], segs[i:]
            if ons in self.attest_ons and cod in self.attest_cod:
                return i
        return None

    def _mark_internal_clusters(self, scores, marks, word):

        def segs2str(segs):
            return ''.join(segs)

        def find_boundary(onset):
            return coda, onset

        st = 'INI'
        coda, onset = [], []
        for i, seg in enumerate(word):
            if st == 'INI':
                if marks[i] == 'N':
                    st == 'NUC'
                    onset, coda = [], []
                elif marks[i] == ' ':
                    marks[i] = 'O'
            elif st == 'NUC':
                if marks[i] in ['N', ')']:
                    pass
                elif marks == ' ':
                    st == 'INT'
                    onset.append(word[i])
            elif st == 'INT':
                if marks[i] == ' ':
                    onset.append(word[i])
                elif marks[i] == 'N':
                    j = find_boundary(i)  # too few variables for assignment!
                    st = 'NUC'

    def _mark_initial_onset(self, marks, nuclei):
        pass

    def _mark_final_coda(self, marks, nulcei):
        pass

    def parse(self, word):
        word = list(panphon.segment_text(word))  # Divide into segments.
        scores = map(lambda x: self.ft.sonority(x), word)  # Sonority scores.
        cons = len(scores) * [' ']
        cons, nuclei = self._mark_peaks_as_nuclei(scores, cons)
        cons = self._mark_glides(scores, cons, nuclei)
