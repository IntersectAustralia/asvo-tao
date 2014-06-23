"""
Test: MI01

Description:

* Ensure that Mock Image can run on light-cone geometry and doesn't crash

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
REPETITION = 'Random'
SIMULATION = 'Millennium'
GALAXY_MODEL = 'SAGE'
RA = 2
DEC = 2
REDSHIFT_MIN = 0.3
REDSHIFT_MAX = 0.5
NUMBER_OF_CONES = 1


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
#
# BP_FILTERS is either the key-string 'All', or a list of search criteria,
# e.g. 'SDSS' would add all SDSS filters
#
BP_FILTERS = ['SDSS u (Apparent)', 'GALEX FUV (Apparent)']

#
# Mock Image
#
APPLY_MOCK_IMAGE = True
#
# An image will be created for each set of parameters
#
# "__prefix__-min_mag"
# "__prefix__-max_mag"
# "__prefix__-z_min"
# "__prefix__-z_max"
# "__prefix__-origin_ra"
# "__prefix__-origin_dec"
# "__prefix__-fov_ra"
# "__prefix__-fov_dec"
# "__prefix__-width"
# "__prefix__-height"
#
MI_PARAMS = []

#
# Record Selection properties
#
FILTER_MIN = '1.0'
FILTER_MAX = ''


#
# Specify the results validator
#
from cone_basic import Validator as v1
from mi_basic import Validator as v2
VALIDATORS = [v1, v2]
