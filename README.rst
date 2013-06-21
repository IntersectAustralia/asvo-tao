============================================
Theoretical Astrophysical Obversvatory (TAO)
============================================

Description
===========

The Theoretical Astrophysical Obvservatory (TAO) is a service hosted and supported by the `Centre for Astrophysics and Supercomputing <http://astronomy.swin.edu.au/>`_ at the `Swinburne University of Technology <http://www.swinburne.edu.au/>`_ to facilitate research in to the galaxy formation and the evolution of the universe.

For more information about TAO and the ASVO, please see the `ASVO Web Site <http://asvo.org.au>`_.

Web UI
======

The TAO UI is a Python / Django hosted application.  The installation instructions below assume that virtualenv is being used to isolate the environment.

Major Dependencies
------------------

================== ========
Module             Version
================== ========
libxml2-dev
libxslt-dev
libmysqlclient-dev
Python             >= 2.6.5
Python-dev
doxygen
virtualenv         >= 1.9.1
Apache (optional)
================== ========

The remaining python modules are listed in tao.pip.reqs.

Initial Environment Configuration
---------------------------------

Follow the steps below to set up your virtual environment and check out the code.  Additional information is then available in the online documentation.::

   #
   # Set up the virtual environment
   #
   virtualenv tao
   cd tao
   source bin/activate
   #
   # Get the code
   #
   git clone git@github.com:IntersectAustralia/asvo-tao.git
   #
   # Install all the required python libraries
   #
   cd asvo-tao
   # Temporary until this is merged in to work & master
   git checkout asvo-414-replace-buildout
   # end temporary
   pip install -r tao.pip.reqs
   #
   # Set up paths, etc.
   #
   cd ../bin
   ln -s ../asvo-tao/web/manage.py
   #
   # Build the documentation
   #
   cd ../asvo-tao/docs
   ./gendoc.sh
   gnome-open build/index.html
   # Continue with the instructions in the Developer's Guide:
   # - asvo-tao/docs/build/developers/index.rst
   # - http://tao.asvo.org.au/taodemo/static/docs/developers/index.html


