Known Issues
============

.. contents::
   :depth: 2

Fixed maximum execution time
----------------------------

The maximum allowed execution time for a job is currently fixed at 48 hours without any indication of whether a job is likely to finish within the allowed time or not.

A future update to TAO will:

# Provide feedback prior to submitting a job on whether it is likely to complete within the allowed time
# Give some indication on how large the resulting catalogue is likely to be

Details of how these will be indicated are still to be determined.


Multiple unique light cones have the same observation point
-----------------------------------------------------------

When generating multiple unique light cones the same observation point is used for all of the catalogues, resulting in the same cone being generated.  A different observation point should be selected for each cone to ensure that no part of the simulation space is used in multiple light-cones.


Input Validation is late
------------------------

The New Catalogue wizard currently leaves some input validation until the Submit button is pressed, instead of when moving to the next tab within the wizard.


Number of light cones widget
----------------------------

The counter widget for selecting the number of light cones  is inconsistent in its behaviour, sometimes changing value when the mouse is moved over the counter buttons, and displaying warnings at unexpected times.

