#!/usr/bin/env python

import sys
import warnings
import astropy.io.votable.exceptions
from astropy.io.votable import parse_single_table

if len(sys.argv) < 2:
    print "\nplease specify an input file.\n"
    sys.exit()

filename = sys.argv[1]

# suppress version mismatch warning
warnings.filterwarnings(action='ignore', category=astropy.io.votable.exceptions.W21)

# suppress invalid unit warnings
warnings.filterwarnings(action='ignore', category=astropy.io.votable.exceptions.W50)

# enforce utf-8 encoding
reload(sys)
sys.setdefaultencoding("utf-8")

# load data
table = parse_single_table(filename)
data = table.array

# Read comlumn names
columns = []
for field in table.fields:
	columns.append(field.name)

# Print out the header 
print "#", ", ".join("%s" % c for c in columns)

# Print out the dataset
for i in range(0,len(data[columns[0]])):
    d = []
    for j in range(0,len(columns)):
    	d.append(data[columns[j]][i])
    print " ".join("%e" % c for c in d)
