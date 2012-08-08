========================
ASVO-TAO Science Modules
========================

Description
===========
These are the science modules, designed to carry out the HPC operations, such
as building a lightcone and calculating the SEDs.

Dependencies
============

  Python
    An object-oriented interpreted programming language.

  SCons
    A Python based build system.

  scons-config
    Some SCons configuration helper scripts. This is available from my github
    page at <http://github.com/furious-luke/scons-config>.

  scons-project
    Some SCons C++ project helper scripts. This is available from my github
    page at <http://github.com/furious-luke/scons-config>.

  BOOST
    A set of efficient C++ extensions.

  MPI
    Message Passing Interface implementation. Tested with MPICH2 and OpenMPI.

  HDF5
    Hierarchical Data Format libraries. Currently tested with version 1.8.7.

  libhpc
    A collection of wrappers and structures to help high-performance
    programming, <http://github.com/furious-luke/libhpc>.

Installation
============

The science modules use SCons as the build system. At a minimum, you will need
to install:

  Python 2.7+
    This can probably be installed using your operating system's package
    management. Alternatively visit `the Python homepage <http://python.org>`_
    to download it manually.

  SCons
    Like Python, you're operating system likely has a package for this, or
    visit `the SCons homepage <http://scons.org>`_.

  scons-config
    Download from `here <http://github.com/furious-luke/scons-config>`_.

  scons-project
    Download from `here <http://github.com/furious-luke/scons-project>`_.

The remaining dependencies (Boost, MPI, HDF5, etc) can either be installed
manually, or can be automatically downloaded and installed specifically for
use by the science modules by building the science modules source with the
command::

  scons DOWNLOAD_ALL=yes

If you want to install the dependencies manually, then once they are ready you
may build the science modules with the command::

  scons

You may need to specify the locations of some of the dependencies. To see a
list of options for doing so, along with various other build options, run::

  scons -h
