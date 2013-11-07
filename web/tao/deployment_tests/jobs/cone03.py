"""
Test: Cone01

Description:

* Ensure galaxies are within requested geometry: RA=90, Dec=2

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
REPETITION = 'Random'
SIMULATION = 'Millennium'
GALAXY_MODEL = 'SAGE'
RA = 90
DEC = 2
REDSHIFT_MIN = 0.0
REDSHIFT_MAX = 0.3
NUMBER_OF_CONES = 1

#
# Define the list of output properties to use.
#
OUTPUT_PROPERTIES = 'All'


#
# Record Selection properties
#
FILTER_MIN = '0.1'
FILTER_MAX = ''


#
# Specify the results validator
#
#GALAXY_COUNT = 833155
#CHECK_UNIQUE = True
from cone_basic import Validator as v1
VALIDATORS = [v1]
