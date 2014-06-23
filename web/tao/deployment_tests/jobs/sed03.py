"""
Test: Sed03

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
SIMULATION = 'Millennium'
GALAXY_MODEL = 'SAGE'
RA = 8
DEC = 8
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
BP_FILTERS = ['Johnson']

#
# Record Selection properties
#
FILTER_MIN = '0.31'
FILTER_MAX = ''


#
# Specify the results validator
#
LITTLE_H = 0.73
WM = 0.25
MIN_MEAN_DIFFERENCE = 4 # %
MAX_MEAN_DIFFERENCE = 5 # %
MIN_MAX_DIFFERENCE = 7 # %
MAX_MAX_DIFFERENCE = 8 # %
from sed_distance import Validator as v1
VALIDATORS = [v1,]
