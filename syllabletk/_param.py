# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from collections import Counter


class ParameterizedSyllabifier(object):

    def __init__(self, initial, final):
        self.onsets, self.nuclei, self.codas = Counter(), Counter(), Counter()

    def get_counters(self):
        return (self.onsets, self.nuclei, self.codas)
