#!/usr/bin/env python

import sys
from decimal import Decimal
from analytic import generate

a = Decimal(2)
b = Decimal(3)

def func(x):
    return a

def bp_func(x):
    return b

if __name__ == '__main__':
    generate(int(sys.argv[1]), int(sys.argv[2]), Decimal(sys.argv[3]), Decimal(sys.argv[4]), func, bp_func)
