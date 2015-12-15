# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from collections import Counter
import panphon
import logging

logging.basicConfig(logging=logging.DEBUG)


class MarginMinder(object):

    def __init__(self, margin_parser):
        self.margin_parser = margin_parser()
        self.initial, self.final = Counter(), Counter()

    def parse_tokens(self, tokens):
        for token in tokens:
            initial, final = self.margin_parser.parse(token)
            self.initial.update(initial)
            self.final.update(final)


class WordMarginParser(object):

    def __init__(self):
        self.ft = panphon.FeatureTable()

    def _sonority_map(self, word):
        return map(self.ft.sonority, word)

    def from_map(self, son_map, word):
        return ''.join([x for (x, _) in zip(word, son_map)])

    def from_reverse_map(self, son_map, word):
        return self.from_map(son_map[::-1], word[::-1])[::-1]


class FixedSonoritySlicer(WordMarginParser):

    def _initial_onset(self, son_map):
        i = 0
        ons = ''
        while son_map[i] < 8 and i < len(son_map):
            ons += '{}'.format(son_map[i])
            i += 1
        return ons

    def _final_coda(self, son_map):
        i = len(son_map) - 1
        cod = ''
        while son_map[i] < 8 and i > 0:
            cod = '{}'.format(son_map[i]) + cod
            i -= 1
        return cod

    def parse(self, word):
        son_map = self._sonority_map(word)
        ons_son = self._initial_onset(son_map)
        cod_son = self._final_coda(son_map)
        ons = self.from_map(ons_son, word)
        cod = self.from_reverse_map(cod_son, word)
        return (ons, cod)


class SonorityPeakSlicer(WordMarginParser):

    def _mark_offglides(self, son_map):
        state = 'C'
        for i, son in enumerate(son_map):
            if son > 7:
                state = 'V'
            if state == 'V' and son == 7:
                son_map[i] = son_map[i - 1]
            if son <= 7:
                state == 'C'
        return son_map

    def _adjust_anom_fric_ons(self, son_map):
        length = len(son_map)
        i = 0
        while i < length - 2 and son_map[i] < 5:
            if son_map[i] in [3, 4] and son_map[i + 1] in [1, 2]:
                son_map[i] = son_map[i] - 2
            i += 1
        return son_map

    def _adjust_anom_fric_cod(self, son_map):
        length = len(son_map)
        i = length - 1
        while i > 0 and son_map[i] < 5:
            if son_map[i] in [3, 4] and son_map[i - 1] in [1, 2]:
                son_map[i] = son_map[i] - 2
            i -= 1
        return son_map

    def _initial_onset(self, son_map):
        length = len(son_map)
        i = 0
        ons = []
        if length == 1:
            return []
        else:
            while i < length - 1 and son_map[i] <= son_map[i + 1]:
                ons.append(son_map[i])
                i += 1
            while len(ons) > 1 and ons[-1] > 7:
                ons.pop()
            return ons

    def _final_coda(self, son_map):
        length = len(son_map)
        i = length - 1
        ons = []
        if length == 1:
            return []
        else:
            while i > 0 and son_map[i] <= son_map[i - 1]:
                ons.insert(0, son_map[i])
                i -= 1
            while len(ons) > 1 and ons[0] > 7:
                ons.pop(0)
            return ons

    def parse(self, word):
        son_map = self._sonority_map(word)
        son_map = self._mark_offglides(son_map)
        son_map = self._adjust_anom_fric_cod(son_map)
        son_map = self._adjust_anom_fric_ons(son_map)
        ons_son = self._initial_onset(son_map)
        cod_son = self._final_coda(son_map)
        ons = self.from_map(ons_son, word)
        cod = self.from_reverse_map(cod_son, word)
        return (ons, cod)
