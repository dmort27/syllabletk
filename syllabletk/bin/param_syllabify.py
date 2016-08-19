#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from syllabletk import ParameterizedSyllabifier, PhonoRepr
import argparse
import sys
import yaml


def prettify_syllables(word):
    s = ''
    for o, n, c in word:
        o = ''.join(o)
        n = ''.join(n)
        c = ''.join(c)
        s = s + '({}-{}-{})'.format(o, n, c)
    return s

def flatten_syllables(word):
    s = ''
    for o, n, c in word:
        s += ''.join(o)
        s += ''.join(n)
        s += ''.join(c)
    return s


def main(margins):
    with open(margins) as f:
        margin_dict = yaml.load(f.read())
    initials = margin_dict['initials'].keys()
    finals = margin_dict['finals'].keys()
    ps = ParameterizedSyllabifier((initials, finals))
    for line in sys.stdin:
        word = line.strip().decode('utf-8')
        print('word={}'.format(word).encode('utf-8'))
        syllabified = ps.syllabify(word)
        if syllabified:
            pretty = prettify_syllables(syllabified)
            flat = flatten_syllables(syllabified)
            print('"{}" -> {}'.format(word, pretty).encode('utf-8'), file=sys.stdout)
            assert word.replace('ʼ', '') == flat

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Uses syllable margins as parameters to parse a list of words.')
    parser.add_argument('margins', help='PyYAML file containing syllable margins from list')
    args = parser.parse_args()
    main(args.margins)
