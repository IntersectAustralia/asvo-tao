What's New
==========

.. contents::
   :depth: 2

9 Dec 2013: 1.0.15
------------------

Improvements:

* Updated welcome page text
* Additional deployment tests

Bug Fixes:

* Update details tab when using keyboard navigation within two-list widgets (ASVO-464)


25 Nov 2013: 1.0.13
-------------------

Improvements:

* Indent Survey Presets in the UI to better distinguish between Start choices and Survey Preset choices (ASVO-663).
* Disable Selection (record filter) on magnitudes (until performance can be optimised) (ASVO-670).
* Enable access to params.xml & summary.txt during catalogue generation (ASVO-661).
* Registration rejection email is now optional (ASVO-657)


Bug Fixes:

* Correct URL in README (was pointing to the old demo site)
* summary.txt now displays the SSP label instead of the internal id (ASVO-658)
* Clear selected Output Properties when changing datasets (ASVO-662)


11 Nov 2013: 1.0.12
-------------------

Improvements:

* Disallow Absolute magnitudes in the Mock Image module.
  These tend to over expose the image or cause the job to fail due to SkyMaker running out of time or memory.
* Change History page sub-title to "TAO - Catalogues" (and avoid IT jargon)

Bug Fix:

* Undo production.py accidental over-write


7 Nov 2013: 1.0.11
------------------

Bug Fixes:

* The selected Output Properties in the General Properties tab are cleared when changing datasets.
* Mock Image now uses 0 based indexing when referencing the sub-cone.
* Cone geometry has been fixed for light-cones with an opening angle of 90 degrees.


4 Nov 2013: 1.0.10
------------------

Major Changes:

* The Password Reset page now includes an email address in case you have problems with password reset.
* The TAP Server now encodes queries without a record limit correctly.
* The Change Password link is again available for system administrators.


31 Oct 2013: 1.0.8
------------------

Major Changes:

* We have added a new category of autmated tests: deployment tests.
  Along with the current unit and integration tests,
  these help ensure that the system as deployed is operating in the same was as
  in the test environment.
* Additional input validation: check that the redshift minimum and maximum
  values are less than the simulation maximum redshift.
* Improved handling of malformed XML in params.xml.


24 Oct 2013: 1.0.7
------------------

Major Changes:

* The default Selection Filter has been removed.
  This means that the user must select a filter explicitly,
  removing the chance of a catalogue with unexpected filtering being produced.
* Mock Image field validation has been improved.
* The User Disk Quota is displayed along with Disk Usage in the History page.
 
