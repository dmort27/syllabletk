# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import panphon
# import logging
import regex as re

# logging.basicConfig(level=logging.DEBUG)


class PhonoRepr(object):
    """Multi-tiered representation of a phonological word.

    Args:
    segs -- Segments as a list of unicode strings.
    ft -- panphon.FeatureTable object.

    Members:
    marks -- Marks that indicate whether the corresponding segment is an onset
    ("O"), nucleus ("N"), offglide (")"), or coda ("C").
    scores -- sonority scores for the corresponding segment.
    i -- index for operations that scan the string.
    """

    def __init__(self, ft, word):
        self.segs = list(panphon.segment_text(word))
        self.marks = [' ' for s in self.segs]
        self.scores = [ft.sonority(s) for s in self.segs]
        self.nuclei = []
        self.syl_regex = re.compile('(O*)(NG?)(C*)')

    def get_segment(self, i=None):
        """Return segment, sonority score, and mark for the index.

        i -- the index to use; if unspecified or set to None, self.i is used
        instead.
        """
        i = i if i is not None else self.i
        return self.segs[i], self.scores[i], self.marks[i]

    def set_mark(self, i, symbol):
        """Set the mark at the index.

        i -- the index.
        symbol -- one of "O", "N", "C", or "G".
        """
        self.marks[i] = symbol
        if symbol == 'N':
            self.nuclei.append(i)
            self.nuclei.sort()

    def syllabified(self):
        """Return segments syllabified according to the marks."""
        segs = self.segs[:]
        segs_syl = []
        for m in self.syl_regex.finditer(''.join(self.marks)):
            o, n, c = m.groups()
            ons = segs[0:len(o)]
            segs = segs[len(o):]
            nuc = segs[0:len(n)]
            segs = segs[len(n):]
            cod = segs[0:len(c)]
            segs = segs[len(c):]
            segs_syl.append((ons, nuc, cod))
        return segs_syl


class ParameterizedSyllabifier(object):
    """Syllabifier that takes sniffed word-margin data as a parameter.

    margins -- a 2-tuple of the form <init, fin> that provides attested onsets
    and codas to the syllabifier. Since these constituents are known to be
    possible onsets and codas, they are considered to be licit whenever they
    occur. When a sequence of consonants between nuclei cannot be divided into
    an onset from self.attest_ons and a coda from attest_cod, sonority is used
    as a fallback.
    """

    def __init__(self, margins):
        self.attest_ons, self.attest_cod = margins
        self.attest_ons.sort(key=lambda x: len(x), reverse=True)
        self.attest_cod.sort(key=lambda x: len(x), reverse=True)
        self.ons_set = {tuple(x) for x in self.attest_ons}
        self.cod_set = {tuple(x) for x in self.attest_cod}
        self.ft = panphon.FeatureTable()

    def _longest_ons_prefix(self, phonr):
        """Mark and return longest onset prefix.

        phonr -- a PhonoRepr object with the longest onset prefix, if any,
        marked.
        """
        i = len(phonr.segs)
        while tuple(phonr.segs[:i]) not in self.ons_set and i > 0:
            i -= 1
        phonr.set_mark(i, 'N')
        for j in range(i):
            phonr.set_mark(j, 'O')
        return phonr

    def _longest_cod_suffix(self, phonr):
        """Mark and return longest coda suffix.

        phonr -- a PhonoRepr object with the longest coda suffix, if any, marked.
        """
        i = 0
        while tuple(phonr.segs[i:]) not in self.cod_set and i < len(phonr.segs):
            i += 1
        phonr.set_mark(i - 1, 'N')
        for j in range(i, len(phonr.segs)):
            phonr.set_mark(j, 'C')
        return phonr

    def _mark_rem_nuclei(self, phonr):
        """Marks remaining nuclei after first and last nuclei are marked.

        phonr -- a PhonoRepr object.
        return -- a mutated PhonoRepr object with all nuclei marked.
        """
        first, last = phonr.nuclei[0], phonr.nuclei[-1]
        if first == last:
            return phonr
        for i, score in zip(range(first, last), phonr.scores[first:last]):
            if score > 7:
                phonr.set_mark(i, 'N')
            elif score > phonr.scores[i - 1] and \
                    score > phonr.scores[i + 1]:
                phonr.set_mark(i, 'N')
        return phonr

    def _mark_offglides(self, phonr):
        """Mark glides after vowels with 'G'.

        phonr -- a PhonoRepr object.
        return -- mutated PhonoRepr object with postvocalic glides marked.
        """
        state = ' '
        for i, mark in enumerate(phonr.marks):
            if state == 'N' and mark == ' ' and phonr.scores[i] == 7:
                phonr.set_mark(i, 'G')
            state = mark
        return phonr

    def _mark_intervocalic_clusts(self, phonr):
        """Mark the clusters between vowels with 'C's and 'O's.

        phonr -- a PhonoRepr object.
        return -- mutated PhonoRepr object.
        """
        if len(phonr.nuclei) > 1:
            for i, start in enumerate(phonr.nuclei[:-1]):
                end = phonr.nuclei[i + 1]
                if self._mark_intervocalic_clust_attested(phonr, start, end) is None:
                    self._mark_intervocalic_clust_sonority(phonr, start, end)
        return phonr

    def _mark_intervocalic_clust_attested(self, phonr, start, end):
        """Use attested onsets/codas to mark intervocalic consonants/clusters.

        phonr -- a PhonoRepr object.
        start -- index marking the beginning of a consonant sequence.
        end -- index marking the end of a consonant sequence.
        return -- mutated phonr if syllabificiation is possible; otherwise, None.
        """
        while phonr.marks[start + 1] == 'G':
            start += 1
        for i in range(start + 1, end):
            cod = phonr.segs[start + 1:i]
            ons = phonr.segs[i:end]
            if tuple(cod) in self.cod_set and tuple(ons) in self.ons_set:
                for j in range(start + 1, i):
                    phonr.set_mark(j, 'C')
                for j in range(i, end):
                    phonr.set_mark(j, 'O')
                return phonr
        return None

    def _mark_intervocalic_clust_sonority(self, phonr, start, end):
        """Use sonority to mark intervocalic consonants/clusters.

        phonr -- a PhonoRepr object.
        start -- index marking the beginning of a consonant sequence.
        end -- index marking the end of a consonant sequence.
        return -- mutated phonr if syllabificiation is possible; otherwise, None.
        """

        def valid_cod(cod):
            for i, score in enumerate(cod[:-1]):
                if i < len(cod) - 1 and score < cod[i + 1]:
                    return False
            return True

        def valid_ons(ons):
            return valid_cod(list(reversed(ons)))

        for i in range(start + 1, end):
            cod = phonr.scores[start + 1:i]
            ons = phonr.scores[i:end]
            if valid_cod(cod) and valid_ons(ons):
                for j in range(start + 1, i):
                    phonr.set_mark(j, 'C')
                for j in range(i, end):
                    phonr.set_mark(j, 'O')
                return phonr
        return None

    def syllabify(self, word):
        """Syllabify word into a list of tuples of lists.

        word -- Unicode IPA string to be syllabified.
        return -- a list of 3-tuples (syllables) consisting of lists of strings.
        """
        phonr = self.PhonoRepr(self.ft, word)
        phonr = self._longest_ons_prefix(phonr)
        phonr = self._longest_cod_suffix(phonr)
        phonr = self._mark_rem_nuclei(phonr)
        phonr = self._mark_offglides(phonr)
        phonr = self._mark_intervocalic_clusts(phonr)
        # return phonr.syllabified()
