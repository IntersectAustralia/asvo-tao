#!/usr/bin/env python

def cat(ptrn, n_files, out_fn, **kwargs):
    skip = kwargs.get('skip', 0)
    with open(out_fn, 'w') as out_f:
        for ii in xrange(n_files):
            with open(ptrn%ii, 'r') as in_f:
                for jj in range(skip):
                    in_f.readline()
                out_f.write(in_f.read())

if __name__ == '__main__':
    import sys, argparse

    parser = argparse.ArgumentParser(description='Concatenate files.')
    parser.add_argument('pattern', help='input pattern')
    parser.add_argument('n_files', type=int, help='number of files')
    parser.add_argument('output', help='output filename')
    parser.add_argument('--skip', '-s', type=int, default=0, help='skip lines')
    args = parser.parse_args()

    cat(args.pattern, args.n_files, args.output, skip=args.skip)
