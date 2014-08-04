#!/usr/bin/env python

import sys, argparse
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Plot a histogram.')
parser.add_argument('filename', help='input filename')
parser.add_argument('column', type=int, help='column to use')
parser.add_argument('-s', '--seperator', help='parse seperator')
parser.add_argument('--xl', dest='min_x', default=None, help='minimum x')
parser.add_argument('--xu', dest='max_x', default=None, help='maximum x')
parser.add_argument('--log', type=bool, default=False, help='maximum x')
args = parser.parse_args()

x = []
with open(args.filename, 'r') as in_f:
    for line in in_f:
        words = line.split(args.seperator)
        try:
            val = float(words[args.column])
        except:
            print 'ERROR: Parse error on line: %s'%line
            continue
        if args.log:
            if val > 0.0:
                x.append(math.log10(val))
        else:
            x.append(val)

plt.figure(figsize=(12.8,12.8), dpi=80)
plt.hist(x, bins=75)
plt.xlim([args.min_x, args.max_x])
# plt.title('Mass Errors')
# plt.xlabel('percentage mass difference')
plt.ylabel('frequency')
plt.savefig('figure.png')
