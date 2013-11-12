"""
Test: Cone04

Description:

* Ensure galaxies are unique for a Bolshoi deep pencil cone: RA=Dec=1, z=0.7

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
SIMULATION = 'Bolshoi'
GALAXY_MODEL = 'SAGE'
RA = 1
DEC = 1
REDSHIFT_MIN = 0.0
REDSHIFT_MAX = 0.7
NUMBER_OF_CONES = 2

#
# Define the list of output properties to use.
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
#GALAXY_COUNT = 833155
CHECK_UNIQUE = True
from cone_basic import Validator as v1
VALIDATORS = [v1]
