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

    def decr(self):
        """Decrement the oject index."""
        self.i -= 1

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

    def _longest_ons_prefix(self, phonr):
        """Return the longest prefix of phonr.segs that is an attested onset.

        phonr - a PhonoRepr object
        """
        while phonr.string_before() in self.attest_ons:
            phonr.incr()
        return phonr.string_before(phonr.i - 1)

    def _suffix_is_coda(self, phonr):
        """Return True if segs form attested coda.

        phonr - a PhonoRepr object
        """
        return phonr.string_after() in self.attest_cod

    def _mark_init_ons_nuc(self, phonr):
        pass

    def _mark_offglide(self, phonr):
        pass
