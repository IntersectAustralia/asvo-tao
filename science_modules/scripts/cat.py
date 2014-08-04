#!/usr/bin/env python

def cat(ptrn, n_files, out_fn):
    with open(out_fn, 'w') as out_f:
        for ii in xrange(n_files):
            with open(ptrn%ii, 'r') as in_f:
                in_f.readline()
                out_f.write(in_f.read())

if __name__ == '__main__':
    import sys
    cat(sys.argv[1], int(sys.argv[2]), sys.argv[3])
