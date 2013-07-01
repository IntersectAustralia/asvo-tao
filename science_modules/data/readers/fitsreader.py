#!/usr/bin/env python

import pyfits
import sys

if len(sys.argv) < 2:
    print "\nplease specify an input file.\n"
    sys.exit()

filename = sys.argv[1]

data = pyfits.open(filename)

# Read comlumn names
n_fields = data[1].header['TFIELDS']
fields = []
for i in range(1,n_fields+1):
    fields.append(data[1].header['TTYPE%d' % i])

# Print out the header
print "#", ", ".join("%s" % f for f in fields)

# Print out the dataset
for i in range(0, len(data[1].data)):
    vars = []
    for j in range(0,n_fields):
    	vars.append(data[1].data[i][j])
    print " ".join("%e" % v for v in vars)

        