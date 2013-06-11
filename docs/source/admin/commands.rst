Management CLI Commands
=======================

TAO provides a number of utilities to assist with managing the installation, built on `Django's Management Command framework <https://docs.djangoproject.com/en/dev/howto/custom-management-commands/>`_.

To list all available commands type::

   manage.py

To get help on a particular command, use the help command::

   manage.py help

or::

   manage.py help <command>

e.g.::

   manage.py help add_bpfilters

A brief description of the TAO commands is provided below.  For details on how to use the command, please see the commands help.

add_bpfilters
-------------

Add the specified bandpass filters to the Master DB, generate spectra and link to the documentation from the filter details tab.

See also the Administration Guide on managing BandPass Filters.


tao_jobctl
----------

Submit and list jobs in TAO.

tao_jobctl is useful as it allows multiple jobs to be quickly submitted when testing the system, and for re-submitting jobs (if you like using the command line).

