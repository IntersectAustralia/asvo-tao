"""
Test: Box01

Description:

This tests:

* A box geometry catalogue can be generated
* The coordinates of the galaxies are within the Simulation size
* The number of galaxies in the box is as expected
"""

from common_settings import *

#
# General details
#
DESCRIPTION = "Deployment Test: " + __name__

#
# General Properties
#
GEOMETRY = 'Box'
SIMULATION = 'Bolshoi'
GALAXY_MODEL = 'SAGE'
BOX_SIZE = 250
# Note: REDSHIFT needs to be entered here as it appears on the web page
REDSHIFT = '0.0000'
#
# Define the list of output properties to use.
#
# Currently ignored, and all properties are always added
#
OUTPUT_PROPERTIES = 'All'


#
# Record Selection properties
#
FILTER_MIN = '1.0'
FILTER_MAX = ''


#
# Specify the results validator
#
GALAXY_COUNT = 282384
COORDINATE_MIN_RANGE = [0.0, 0.1]
COORDINATE_MAX_RANGE = [249.9, 250.0]
from box_basic import Validator as v1
VALIDATORS = [v1,]
