"""
Test: MI02

Description:

* Ensure that the Mock Image magnitude filter is doing its job.

This is tested by generating three images from a single cone and the visually
checking that the images are different.

The test generates the images and the validation downloads and unpacks them.
It's up to you to visually inspect the images.
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
# Params File - must be a relative path
#
PARAMS_FILE = 'jobs/mi02.xml'

#
# Specify the results validator
#
from cone_basic import Validator as v1
from mi_basic import Validator as v2
VALIDATORS = [v1, v2]
