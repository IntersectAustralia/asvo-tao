#!/usr/bin/env python

import math
from decimal import Decimal
from analytic import run
from generate import A, B, C

c = Decimal(2.99792458e18)

def analytic_enum(ll, lu):
    ll = float(ll)
    lu = float(lu)
    A_ = float(A)
    B_ = float(B)
    C_ = float(C)
    r = (A_*C_)*((1.0/B_)*(math.cos(B_*ll) - math.cos(B_*lu)) + lu - ll)
    return Decimal(r)

def analytic_denom(ll, lu):
    return C*c*(1/ll - 1/lu)

if __name__ == '__main__':
    run(analytic_enum, analytic_denom)
