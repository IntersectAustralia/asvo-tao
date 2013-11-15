#!/usr/bin/env python

import sys, math
from decimal import Decimal
from analytic import generate

A = Decimal(2)
B = Decimal(1e-2)
C = Decimal(1)

def func(x):
    return A*(Decimal(math.sin(B*x)) + Decimal(1.0))

def bp_func(x):
    return C

if __name__ == '__main__':
    generate(int(sys.argv[1]), int(sys.argv[2]), Decimal(sys.argv[3]), Decimal(sys.argv[4]), func, bp_func)
