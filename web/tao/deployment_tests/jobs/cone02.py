"""
Test: Cone02

Description:

* Large number of small unique light-cones
* Unique Cone tests

Typical execution: 
"""

from common_settings import *


#
# Test Properties
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
RA = 20
DEC = 20
REDSHIFT_MIN = 0.0
REDSHIFT_MAX = 0.1
NUMBER_OF_CONES = 8

#
# Define the list of output properties to use.
#
# Currently ignored, and all properties are always added
#
OUTPUT_PROPERTIES = 'All'


#
# Record Selection properties
#
FILTER_MIN = '0.031'
FILTER_MAX = ''


#
# Specify the results validator
#
GALAXY_COUNT = 52264
CHECK_UNIQUE = True
from cone_basic import Validator as v1
VALIDATORS = [v1]
