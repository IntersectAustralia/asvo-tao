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

##
##
##
def calc_range(array):
    rng = None
    for a in array:
        if not rng:
            rng = [a, a]
        else:
            if a < rng[0]:
                rng[0] = a
            if a > rng[1]:
                rng[1] = a
    return rng

##
##
##
def is_logarithmic(waves):

    # Calculate the mean.
    wcopy = list(waves)
    wcopy.sort()
    avg = 0.0
    for ii in range(len(wcopy) - 1):
        avg += waves[ii + 1] - waves[ii];
    avg /= len(wcopy) - 1;

    # Calculate the variance.
    var = 0.0
    for ii in range(len(wcopy) - 1):
        var += ((waves[ii + 1] - waves[ii]) - avg)**2;
    var /= len(wcopy) - 1;

    # Now the standard deviation.
    dev = math.sqrt(var)

    # If the standard deviation is greater than 1000, use
    # a logarithmic scale.
    return dev >= 1000.0

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
    return waves[ii:jj + 1], values[ii:jj + 1]

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
    x_rng = calc_range(waves)
    y_rng = calc_range(values);

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
    plt.xlim(filter['x_rng'])
    plt.xlabel(ur'Wavelength (\u00c5)')
    if is_logarithmic(filter['waves']):
        plt.xscale('log')
    plt.grid(True)
    plt.title(filter['filter_name'])
    # plt.show()


def plot_filter(filename):
    filter = calc_filter(filename)
    plot(filter)
    plt.savefig(filter['filter_name'] + '.png')
    plt.clf()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Please supply filter filename."
        sys.exit()

    plot_filter(sys.argv[1])

