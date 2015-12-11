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


class FixedSonoritySlicer(object):

    def __init__(self):
        self.ft = panphon.FeatureTable()

    def _sonority_map(self, word):
        return map(self.ft.sonority, word)

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

    def from_map(self, son_map, word):
        return ''.join([x for (x, _) in zip(word, son_map)])

    def from_reverse_map(self, son_map, word):
        return self.from_map(son_map[::-1], word[::-1])[::-1]

    def parse(self, word):
        son_map = self._sonority_map(word)
        ons_son = self._initial_onset(son_map)
        cod_son = self._final_coda(son_map)
        ons = self.from_map(ons_son, word)
        cod = self.from_reverse_map(cod_son, word)
        return (ons, cod)
