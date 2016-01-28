# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from panphon import FeatureTable
from panphon import pat
from collections import Counter


class SyllableAnalyzer(object):
    def __init__(self):
        self.ft = FeatureTable()

    def syl_ons_obs_son(self, (ons, _, __)):
        """SYL_ONSET_OBSTRUENT_SONORANT"""
        if self.ft.match_pattern(pat('[-son][+son]'), ons):
            return ons
        else:
            return None

    def syl_ons_plos_son(self, (ons, _, __)):
        """SYL_ONSET_PLOSIVE_SONORANT"""
        if self.ft.match_pattern(pat('[-son -cont][+son]'), ons):
            return ons
        else:
            return None

    def syl_ons_obs_approx(self, (ons, _, __)):
        if self.ft.match_pattern(pat('[-son][+son +cont -nas]'), ons):
            return ons
        else:
            return None

    def syl_ons_plos_approx(self, (ons, _, __)):
        if self.ft.match_pattern(pat('[-son -cont][+son +cont -nas]'), ons):
            return ons
        else:
            return None

    def syl_ons_obs_obs(self, (ons, _, __)):
        if self.ft.match_pattern(pat('[-son][-son]'), ons):
            return ons
        else:
            return None

    def syl_ons_plos_plos(self, (ons, _, __)):
        if self.ft.match_pattern(pat('[-son -cont][-son -cont]'), ons):
            return ons
        else:
            return None

    def syl_ons_son_son(self, (ons, _, __)):
        if self.ft.match_pattern(pat('[+son][+son]'), ons):
            return ons
        else:
            return None

    def syl_ons_nas_nas(self, (ons, _, __)):
        if self.ft.match_pattern(pat('[-syl +son +nas][-syl +son +nas]'), ons):
            return ons
        else:
            return None

    def syl_ons_complex_2(self, (ons, _, __)):
        if self.ft.match_pattern(pat('[][]'), ons):
            return ons
        else:
            return None

    def syl_ons_complex_3(self, (ons, _, __)):
        if self.ft.match_pattern(pat('[][][]'), ons):
            return ons
        else:
            return None


class SyllableAnalyzer2(object):

    def __init__(self):
        self.ft = FeatureTable()
        self.feature_counter = Counter()
        self.syllable_counter = 0
        self.features = [
            ('SYL_ONSET_COMPLEX_2',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[][]'), o)),
            ('SYL_ONSET_COMPLEX_3',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[][][]'), o)),
            ('SYL_ONSET_COMPLEX_4',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[][][][]'), o)),
            ('SYL_ONSET_OBSTRUENT_OBSTRUENT',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son][-son]'), o)),
            ('SYL_ONSET_PLOSIVE_PLOSIVE',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son -cont][-son -cont]'), o)),
            ('SYL_ONSET_FRICATIVE_FRICATIVE',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son +cont][-son +cont]'), o)),
            ('SYL_ONSET_PLOSIVE_FRICATIVE',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son -cont][-son +cont]'), o)),
            ('SYL_ONSET_FRICATIVE_PLOSIVE',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son +cont][-son -cont]'), o)),
            ('SYL_ONSET_FRICATIVE_PLOSIVE',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[-son +cont][-son -cont]'), o)),
            ('SYL_ONSET_SONORANT_SONORANT',
             lambda (o, _, __): self.ft.match_pattern_seq(pat('[+son][+son]'), o)),
        ]

    def analyze_syllable(self, syl):
        self.syllable_counter += 1
        for name, f in self.features:
            if f(syl):
                self.feature_counter[name] += 1
