"""
Test: Cone01

Description:

* Small number of (relatively) unique light-cones
* Unique Cone tests

Typical execution: 
"""

from common_settings import *


#
# Server details
#
# Use a value of None to prompt during execution
#
DESCRIPTION = "Deployment Test: " + __name__

#
# General Properties
#
GEOMETRY = 'Cone'
REPETITION = 'Unique'
SIMULATION = 'Millennium'
GALAXY_MODEL = 'SAGE'
RA = 10
DEC = 10
REDSHIFT_MIN = 0.0
REDSHIFT_MAX = 0.3
NUMBER_OF_CONES = 2

#
# Define the list of output properties to use.
#
# Currently ignored, and all properties are always added
#
OUTPUT_PROPERTIES = 'All'


#
# Record Selection properties
#
FILTER_MIN = '0.0'
FILTER_MAX = ''


#
# Specify the results validator
#
GALAXY_COUNT = 833155
CHECK_UNIQUE = True
from cone_basic import Validator as v1
VALIDATORS = [v1]
