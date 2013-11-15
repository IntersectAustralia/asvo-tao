#!/usr/bin/env python

from analytic import run
from decimal import Decimal
from generate import a, b

c = Decimal(2.99792458e18)

def analytic_enum(ll, lu):
    return a*b*(lu - ll)

def analytic_denom(ll, lu):
    return b*c*(1/ll - 1/lu)

if __name__ == '__main__':
    run(analytic_enum, analytic_denom)
