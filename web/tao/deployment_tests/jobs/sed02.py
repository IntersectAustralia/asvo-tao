"""
Test: Sed02

Description:

* Run Max's Distance / Distance Modulus check

Typical execution: 
"""

from common_settings import *

#
# Many properties will accept None for the default
# Check the code
#

#
# General details
#
DESCRIPTION = "Deployment Test: " + __name__

#
# General Properties
#
GEOMETRY = 'Cone'
REPETITION = 'Unique'
SIMULATION = 'Bolshoi'
GALAXY_MODEL = 'SAGE'
RA = 2
DEC = 2
REDSHIFT_MIN = 0.0
REDSHIFT_MAX = 0.1
NUMBER_OF_CONES = 1


#
# Define the list of output properties to use.
#
# Currently ignored, and all properties are always added
#
OUTPUT_PROPERTIES = ['Stellar Mass', 'Right Ascension', 'Declination', 'Redshift',
                     'Distance', 'x', 'y', 'z']

#
# SED
#
APPLY_SED = True
SED_SSP = 'Maraston (2005), Salpeter IMF'
BP_FILTERS = ['Johnson']

#
# Record Selection properties
#
FILTER_MIN = '0.031'
FILTER_MAX = ''


#
# Specify the results validator
#
LITTLE_H = 0.70
WM = 0.27
MAX_MEAN_DIFFERENCE = 2.8 # %
MAX_MAX_DIFFERENCE = 1.5 # %
from sed_distance import Validator as v1
VALIDATORS = [v1,]
