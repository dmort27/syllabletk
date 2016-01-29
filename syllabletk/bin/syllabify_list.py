#!/usr/bin/env python
# -*- coding: 'utf-8' -*-
from __future__ import division, print_function, unicode_literals

import sys
import panphon
import syllabletk

class Syllabiflow(object):
    def __init__(self, infile, outfile):
        self.ft = panphon.FeatureTable()
        self.sps = syllabletk.SonorityPeakSlicer()
        self.ps = syllabletk.ParameterizedSyllabifier()

def main(infile, outfile):
    pass

if __name__ == '__main__':
    main(sys.stdin, sys.stdout)
