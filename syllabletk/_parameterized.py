# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import panphon


class PhonoRepr(object):
    """Multi-tiered representation of a phonological word.

    Args:
    segs - Segments as a list of unicode strings.
    ft - panphon.FeatureTable object.

    Members:
    marks - Marks that indicate whether the corresponding segment is an onset
    ("O"), nucleus ("N"), offglide (")"), or coda ("C").
    scores - sonority scores for the corresponding segment.
    i - index for operations that scan the string.
    """

    def __init__(self, segs, ft):
        self.segs = segs
        self.i = 0
        self.marks = len(segs) * [' ']
        self.scores = [ft.sonority(s) for s in segs]

    def get_segment(self, i=None):
        """Return segment, sonority score, and mark for the index.

        i - the index to use; if unspecified or set to None, self.i is used
        instead.
        """
        i = i if i is not None else self.i
        return self.segs[i], self.scores[i], self.marks[i]

    def set_mark(self, i, symbol):
        """Set the mark at the index.

        i - the index.
        symbol - one of "O", "N", "C", or "G".
        """
        self.marks[i] = symbol

    def incr(self):
        """Increment the object index."""
        self.i += 1

    def before(self, i=None):
        """Return the tiers up to self.i.

        Follows the logic of sequence slices.
        i - index; if not specified, the value of self.i is used.
        """
        i = i if i is not None else self.i
        return self.segs[:i], self.scores[:i], self.marks[:i]

    def string_before(self, i=None):
        """Return segments before index as string.

        i - index; if not specified, the value of self.i is used.
        """
        i = i if i is not None else self.i
        return ''.join(self.segs[:i])

    def after(self, i=None):
        """Return the tiers after self.i.

        Follows the logic of sequence slices.
        i - index; if not specified, the value of self.i is used.
        """
        i = i if i is not None else self.i
        return self.segs[i:], self.scores[i:], self.marks[i:]

    def string_after(self, i=None):
        """Return segments after index as string.

        i - index; if not specified, the value of self.i is used.
        """
        i = i if i is not None else self.i
        return ''.join(self.segs[i:])


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

    def _longest_prefix(self, phonrepr):
        while phonrepr.string_before() in self.attest_ons:
            phonrepr.incr()

    def _suffix_is_coda(self, phonr):
        """Return True if segs are attested coda."""
        pass

    def _mark_init_ons_nuc(self, phonr):
        pass

    def _mark_offglide(self, phonr):
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
