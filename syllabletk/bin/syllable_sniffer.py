#!/usr/bin/env python
from __future__ import print_function

import sys
import yaml
from collections import Counter

import syllabletk


def write_frequencies(outfile, initials, finals):
    data = {'initials': dict(initials), 'finals': dict(finals)}
    print(yaml.dump(data).encode('utf-8'), file=sys.stdout)


def main(infile, outfile):
    sps = syllabletk.SonorityPeakSlicer()
    initials, finals = Counter(), Counter()
    for line in infile:
        # print(line.strip(), file=sys.stderr)
        initial, final = sps.parse(line.strip().decode('utf-8'))
        initials[initial] += 1
        finals[final] += 1
    write_frequencies(outfile, initials, finals)


if __name__ == '__main__':
    main(sys.stdin, sys.stdout)
