# -*- coding: utf-8 -*-

import logging
import panphon
import regex as re
from types import ListType

logging.basicConfig(level=logging.DEBUG)


class FailedParse(Exception):
    pass


def count_true(items):
    """Return the number of elements in an iterable that evaluate as true."""
    return len([bool(x) for x in items if x])


class Syllabifier(object):
    """Syllabifies words of text.

    word -- Unicode IPA string
    """
    def __init__(self, word, son_peak=True):
        self.ft = panphon.FeatureTable()
        if son_peak:
            self.son_peak_parse(word)
        else:
            self.son_parse(word)
        self.check_parse()

    def check_parse(self):
        cons = u''.join(self.constituents).encode(u'utf-8')
        word = u''.join(self.word).encode(u'utf-8')
        if u' ' in self.constituents:
            raise FailedParse('Unparsed segments ' +
                              'For "{}" parsed "{}".'.format(word, cons))
        if u'N' not in self.constituents:
            raise FailedParse('No nucleus ' +
                              'For "{}", parsed "{}".'.format(word, cons))

    def son_peak_parse(self, word):

        """Syllabify a word using sonority peaks to identify nuclei and sonority
        slopes to identify onsets and codas. Correctly handles falling-sonority
        diphthongs but does not address rising-sonority diphthongs.

        word -- a word to be syllabified as a Unicode IPA string.
        """

        def trace(cons, caller):
            logging.debug(u'{}\t{}'.format(u''.join(cons), caller))
            logging.debug(u''.join(map(str, scores)))
            logging.debug(u''.join(word))

        def mark_peaks_as_nuclei(scores, cons):
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
                trace(cons, 'nuclei')
            return cons, nuclei

        def mark_glides(scores, cons, nuclei):
            for i in nuclei:
                if i < len(cons) - 1:
                    if cons[i + 1] == u' ' and scores[i + 1] >= 7:
                        cons[i + 1] = u')'
                trace(cons, 'glide')
            return cons

        def mark_left_slopes_as_onsets(scores, cons, nuclei):
            for i in nuclei:
                j = i
                while (j > 0 and cons[j - 1] == u'('):
                    j -= 1
                while (j > 0 and
                       cons[j - 1] == u' ' and
                       scores[j] > scores[j - 1]):
                    cons[j - 1] = u'O'
                    j -= 1
                trace(cons, 'onset')
            return cons

        def mark_right_slops_as_codas(scores, cons, nuclei):
            for i in nuclei:
                j = i
                logging.debug('index j={} before increment.'.format(j))
                while (j < len(cons) - 1 and cons[j + 1] == u')'):
                    j += 1
                    logging.debug('index j={} after glide.'.format(j))
                while (j < len(cons) - 1 and
                       cons[j + 1] == u' ' and scores[j] > scores[j + 1]):
                    cons[j + 1] = u'C'
                    j += 1
                    logging.debug('index j={} after coda.'.format(j))
                trace(cons, 'coda')
            return cons

        def mark_margins(cons):
            i = 0
            while cons[i] == u' ' and i < len(cons) - 1:
                cons[i] = u'O'
                i += 1
            i = 0
            while cons[i] == u' ' and i > 0:
                cons[i] = u'C'
                i -= 1
            trace(cons, 'margins')
            return cons

        word = list(panphon.segment_text(word))
        scores = map(lambda x: self.ft.sonority(x), word)
        cons = len(scores) * [' ']
        cons, nuclei = mark_peaks_as_nuclei(scores, cons)
        cons = mark_glides(scores, cons, nuclei)
        cons = mark_left_slopes_as_onsets(scores, cons, nuclei)
        cons = mark_right_slops_as_codas(scores, cons, nuclei)
        cons = mark_margins(cons)
        self.word = word
        self.constituents = cons

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
        for m in re.finditer(ur'(O*)(\(*N\)*)(C*)', labels):
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
        regexp = self.ft.compile_regex_from_str(u'[-syl -son -cont]' +
                                                u'[-syl +son +cont]')
        return map(lambda x: 1.0 if regexp.match(x) else 0.0,
                   self.the_onsets(ws))

    def the_codas(self, ws):
        codas = []
        for w in ws:
            _, _, cod = zip(*Syllabifier(w).as_tuples())
            codas += cod
        return codas

    def the_simple_codas(self, ws):
        regexp = self.ft
        return map(lambda x: 1.0 if len(x) == 1 else 0.0,
                   self.the_codas(ws))

    def the_complex_codas(self, ws):
        return map(lambda x: 1.0 if len(x) > 1 else 0.0,
                   self.the_codas(ws))

    def the_approximant_obstruent_codas(self, ws):
        regexp = self.ft.compile_regex_from_str(u'[-syl +son +cont]' +
                                                u'[-syl -son -cont]')
        return map(lambda x: 1.0 if regexp.match(x) else 0.0,
                   self.the_codas(ws))
