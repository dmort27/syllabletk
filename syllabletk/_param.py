# -*- coding: utf-8 -*-
"""Parses syllables and counts counstitutents using information from margins.
"""

from __future__ import unicode_literals
from __future__ import print_function

from collections import Counter


class ParameterizedSyllabifier(object):

    def __init__(self, initial, final):
        self.onsets, self.nuclei, self.codas = Counter(), Counter(), Counter()

    def get_counters(self):
        return (self.onsets, self.nuclei, self.codas)
