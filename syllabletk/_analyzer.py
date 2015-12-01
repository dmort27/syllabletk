# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from panphon import FeatureTable
from panphon import pat


class SyllableAnalyzer(object):
    def __init__(self):
        self.ft = FeatureTable()

    def syl_ons_obs_son(self, (ons, _, __)):
        if self.ft.match_pattern(pat('[-son][+son]'), ons):
            return ons
        else:
            return None

    def syl_ons_plos_son(self, (ons, _, __)):
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
