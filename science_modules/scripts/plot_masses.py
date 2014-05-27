#!/usr/bin/env python

import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

tao_masses, model_masses, perc_diff = [], [], []
with open(sys.argv[1], 'r') as inp:
    inp.readline()
    for line in inp:
        words = line.split(',')
        try:
            val_x = float(words[0])
            val_y = float(words[1])
            val_z = float(words[2])
        except:
            print 'ERROR: Parse error on line: %s'%line
            continue
        tao_masses.append(val_x)
        model_masses.append(val_y)
        perc_diff.append(val_z)

plt.figure(figsize=(12.8,12.8), dpi=80)
plt.hist(perc_diff, bins=200)
plt.title('Mass Errors')
plt.xlabel('percentage mass difference')
plt.ylabel('frequency')
plt.savefig('mass_error.png')
