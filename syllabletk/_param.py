# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from collections import Counter


class ParameterizedSyllabifier(object):
    """Parses syllables and counts counstitutents with biases from margins.
    """

    def __init__(self, initial, final):
        self.initial, self.final = initial, final
        self.onsets, self.nuclei, self.codas = Counter(), Counter(), Counter()

    def get_counters(self):
        return (self.onsets, self.nuclei, self.codas)
