#!/usr/bin/env python
import sys
import h5py

if len(sys.argv) < 2:
    print "\nplease specify an input file.\n"
    sys.exit()

filename = sys.argv[1]

data = h5py.File(filename, 'r')

fields = []
for d in data.items():
	if data.get(name=d[0], getclass=True) == h5py.Group:
		for dd in data[d[0]]:
			fields.append("%s/%s" % (d[0], dd))
	else:
		fields.append(d[0])

print "#", ", ".join("%s" % f for f in fields)

for i in range(0,len(data[fields[0]])):
	vars = []
	for field in fields:
		vars.append(data[field][i])

	print " ".join("%e" % v for v in vars)

