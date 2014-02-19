#/usr/bin/env python

import sys

if __name__ == '__main__':

    src_fns = sys.argv[1:]
    results = []
    for fn in src_fns:
        cur_res = set()
        cur_cnt = 0
        with open(fn, 'r') as file:
            file.readline()
            for line in file:
                cur_res.add(int(line.split(',')[0].strip()))
                cur_cnt += 1
        if cur_cnt != len(cur_res):
            print 'Duplicate results in file: ' + fn
        results.append(cur_res)

    tot_size = sum([len(s) for s in results], 0)
    for r in results[1:]:
        results[0] |= r
    if tot_size != len(results[0]):
        print 'Duplicate results across files.'
