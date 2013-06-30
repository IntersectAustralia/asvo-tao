System Overview
===============

Working with TAO
----------------

A number of guiding principles and assumptions have been adopted in the design of TAO:

* The system should be as simple as possible to use, while delivering the required functionality.  In particular, knowledge of SQL is not required.
* The user will need to do further filtering and refinement of the data on their local system.

Each dataset is available as a mini- and full- version.

To get the best value from TAO it is recommended that you follow the high level process outlined below (or tell us a better way so we can improve TAO).

#. Develop your query using the mini- version of the Dataset
#. After confirming that the query is returning the required data (output properties, bandpass filters, etc.), re-run the query on the full Dataset.


Job Status
----------

Once a job has been submitted in TAO it will go through a number of states before being ready to download:

=========== ======================================================
State
=========== ======================================================
HELD        The job is held in the TAO queue and will not be executed until set to submitted by an administrator.
SUBMITTED   The job has been submitted in the web ui and awaiting processing by the workflow.
QUEUED      The job has been submitted for processing on the HPC.
IN PROGRESS The job is currently being executed by the HPC.
COMPLETED   The job has completed and is ready for download.
ERROR       The job terminated abnormally.
=========== ======================================================

