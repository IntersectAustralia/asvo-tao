#!/usr/bin/env python

import sys, argparse
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Plot a histogram.')
parser.add_argument('--file', '-f', nargs='+', help='input filename')
parser.add_argument('--column', '-c', nargs='+', default=[0], type=int, help='column to use')
parser.add_argument('--label', '-l', nargs='+', help='legend label')
parser.add_argument('--seperator', '-s', nargs='+', default=[None], help='parse seperator')
parser.add_argument('--log', nargs='+', default=[False], type=bool, help='logarithmic xaxis')
parser.add_argument('--bins', '-b', type=int, default=75, help='number of bins')
parser.add_argument('--xl', dest='min_x', type=float, default=None, help='minimum x')
parser.add_argument('--xu', dest='max_x', type=float, default=None, help='maximum x')
parser.add_argument('--title', help='title')
parser.add_argument('--xaxis', help='xaxis label')
args = parser.parse_args()

x = [[] for ii in range(len(args.file))]

plt.figure(figsize=(12.8,12.8), dpi=80)
bins = None

for ii in range(len(args.file)):
    log = args.log[ii] if len(args.log) > 1 else args.log[0]
    sep = args.seperator[ii] if len(args.seperator) > 1 else args.seperator[0]
    if sep == ' ':
        sep = None
    with open(args.file[ii], 'r') as in_f:
        for line in in_f:
            words = line.split(sep)
            try:
                val = float(words[args.column[ii]])
            except:
                print 'ERROR: Parse error on line: %s'%line
                continue
            if log:
                if val <= 0.0:
                    continue
                val = math.log10(val)
            if (args.min_x is None or val >= args.min_x) and (args.max_x is None or val <= args.max_x):
                x[ii].append(val)
    cbins = bins if bins is not None else args.bins
    n, cbins, patches = plt.hist(x[ii], bins=cbins, histtype='step' if len(args.file) > 1 else 'bar')
    bins = cbins if bins is None else bins

if args.label:
    plt.legend(args.label)
if args.title is not None:
    plt.title(args.title)
if args.xaxis is not None:
    plt.xlabel(args.xaxis)
plt.ylabel('frequency')
plt.savefig('figure.png')
