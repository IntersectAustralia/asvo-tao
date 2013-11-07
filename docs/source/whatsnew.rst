What's New
==========

.. contents::
   :depth: 2

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
 