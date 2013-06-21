#!/usr/bin/env python

##
## Plot a transmission filter. Provided an ascii transmission
## filter as an argument, this script will generate a PDF image
## of the filter. The filter should be in a file as follows:
##
##   <number of entries>
##   <entry 1>
##   <entry 2>
##   ...
##   <entry number-of-entries>
##
## where
##
##   <number of entries> is an integer number,
##   <entry n> is a line with two number separated by whitespace,
##     the first number being the wavelength in angstroms and the
##     second being the transmission.
##
## For example, a very small filter might look like:
##
##   3
##   100  0.4
##   200  1.0
##   300  0.1
##
## The script accepts one arguments, that being the filename of
## the filter.
##

import sys, math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

##
##
##
def is_logarithmic(waves):

    def expfunc(x, a, b, c):
        return a*np.exp(b*x) + c

    wcopy = list(waves)
    wcopy.sort()

    # If the ratio of x-max : x-min < 10, don't use a logarithmic scale
    # (at least in matplotlib)
    if (wcopy[-1] / wcopy[0]) < 10:
        return False

    # Take a guess at whether it is logarithmic by seeing how well the x-scale
    # fits an exponential curve
    diffs = []
    for ii in range(len(wcopy) - 1):
        diffs.append(wcopy[ii + 1] - wcopy[ii])

    # Fit the diffs to an exponential curve
    x = np.arange(len(wcopy)-1)
    try:
        popt, pcov = curve_fit(expfunc, x, diffs)
    except Exception as e:
        print e
        popt = [0.0, 0.0, 0.0]
        pcov = np.inf

    # If a > 0.5 and covsum < 1000.0
    # use a logarithmic scale.
    if type(pcov) == float:
        # It's probably np.inf
        covsum = pcov
    else:
        covsum = pcov.diagonal().sum()
    res = (covsum < 1000.0) & (popt[0] > 0.5)
    #print "Result = {0}".format(res)
    return res


##
##
##
def strip_zeros(waves, values):
    ii = 0
    while ii < len(values) and values[ii] == 0.0:
        ii += 1
    if ii > 0:
        ii -= 1
    jj = len(values) - 1
    while jj >= 0 and values[jj] == 0.0:
        jj -= 1
    if jj < len(values) - 1:
        jj += 1
    return np.array(waves[ii:jj + 1]), np.array(values[ii:jj + 1])

##
##
##
def calc_filter(filename):

    # Read input file.
    waves = []
    values = []
    with open(filename) as filt_file:
        filt_file.readline()
        for line in filt_file:
            words = line.split()
            waves.append(float(words[0]))
            values.append(float(words[1]))

    # Strip and calculate ranges.
    waves, values = strip_zeros(waves, values)
    x_rng = [waves.min(), waves.max()]
    # Add 5% space on either side of the X-axis
    x_space = (x_rng[1] - x_rng[0]) / 20
    x_rng = [x_rng[0]-x_space, x_rng[1]+x_space]
    y_rng = [0, max(1.1, values.max())]

    # Setup variables.
    filter_name = filename[:filename.rfind('.')]

    # Answer as a dictionary
    filter = {
        'filter_name': filter_name,
        'waves': waves,
        'values': values,
        'x_rng': x_rng,
        'y_rng': y_rng,
        }
    return filter

def plot(filter):
    color = '#ff4444'
    # Plot.
    # plt.plot(waves, values, linewidth=2.0, color='grey')
    plt.fill_between(filter['waves'], filter['values'],
        facecolor=color, color=color)
    plt.ylim([filter['y_rng'][0], filter['y_rng'][1] + 0.1])
    plt.ylabel('Transmission')
    if is_logarithmic(filter['waves']):
        plt.xscale('log')
    plt.xlim(filter['x_rng'])
    plt.xlabel(ur'Wavelength (\u00c5)')
    plt.grid(True)
    plt.title(filter['filter_name'])
    # plt.show()


def plot_filter(filename, dest=None):
    #print("Processing: {0}".format(filename))
    filter = calc_filter(filename)
    plot(filter)
    if dest is None:
        pngname = filter['filter_name'] + '.png'
    else:
        pngname = dest
    plt.savefig(pngname)
    plt.clf()
    return pngname


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Please supply filter filename."
        sys.exit(1)

    plot_filter(sys.argv[1])

