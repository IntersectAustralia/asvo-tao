"""
Test: Sed01

Description:

* Ensure that SED can run on box geometry and doesn't crash

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
GEOMETRY = 'Box'
SIMULATION = 'Mini-Millennium'
GALAXY_MODEL = 'SAGE'
BOX_SIZE = None
# Note: REDSHIFT needs to be entered here as it appears on the web page
REDSHIFT = '2.0700'


#
# Define the list of output properties to use.
#
# Currently ignored, and all properties are always added
#
OUTPUT_PROPERTIES = 'All'

#
# SED
#
APPLY_SED = True
# BP_FILTERS is ignored
BP_FILTERS = 'All'

#
# Record Selection properties
#
FILTER_MIN = '0.0'
FILTER_MAX = ''


#
# Specify the results validator
#
GALAXY_COUNT = None
COORDINATE_MIN_RANGE = [0.0, 0.1]
COORDINATE_MAX_RANGE = [62.4, 62.5]
from box_basic import Validator as v1
VALIDATORS = [v1,]
