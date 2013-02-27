#/usr/bin/env python

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
## The script accepts two arguments, the first being the
## filename of the filter, the second being a flag indicating
## if you wish to use a logarithmic wavelength scale (defaults to
## false).
##

import sys
import matplotlib.pyplot as plt

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Please supply filter filename."
        sys.exit()

    # Read input file.
    waves = []
    values = []
    x_rng = None
    y_rng = None
    with open(sys.argv[1]) as filt_file:
        filt_file.readline()
        for line in filt_file:
            words = line.split()
            waves.append(float(words[0]))
            values.append(float(words[1]))
            if not x_rng:
                x_rng = [waves[0], waves[0]]
            else:
                if waves[-1] < x_rng[0]:
                    x_rng[0] = waves[-1]
                if waves[-1] > x_rng[1]:
                    x_rng[1] = waves[-1]
            if not y_rng:
                y_rng = [values[0], values[0]]
            else:
                if values[-1] < y_rng[0]:
                    y_rng[0] = values[-1]
                if values[-1] > y_rng[1]:
                    y_rng[1] = values[-1]

    # Check for logarithmic graph.
    use_log = False
    if len(sys.argv) >= 3:
        if sys.argv[2].lower() in ['yes', 't', 'true', '1']:
            use_log = True

    # Setup variables.
    filter_name = sys.argv[1][:sys.argv[1].rfind('.')]
    color = '#ff4444'

    # Plot.
    # plt.plot(waves, values, linewidth=2.0, color='grey')
    plt.fill_between(waves, values, facecolor=color, color=color)
    plt.ylim([y_rng[0], y_rng[1] + 0.1])
    plt.ylabel('Transmission')
    plt.xlim(x_rng)
    plt.xlabel(ur'Wavelength (\u00c5)')
    if use_log:
        plt.xscale('log')
    plt.grid(True)
    plt.title(filter_name)
    # plt.show()
    plt.savefig(filter_name + '.pdf')
