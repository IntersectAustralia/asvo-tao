#!/usr/bin/env python

import os
from plot_filter import plot_filter

if __name__ == '__main__':

    # List all filters (extension .dat).
    filters = [f for f in os.listdir(os.getcwd()) if f[-4:].lower() == '.dat']

    # Run on all filters.
    for filt in filters:
        print 'Plotting ' + filt
        plot_filter(filt)
