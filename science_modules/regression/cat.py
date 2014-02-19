base = 'result.filter.csv.%05d'
cnt = 4
with open('result', 'w') as outf:
    for ii in xrange(cnt):
        with open(base%ii, 'r') as inf:
            inf.readline()
            outf.write(inf.read())
