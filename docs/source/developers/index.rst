Developer's Guide
*****************

This is currently more of a dumping ground than an organised guide - it should improve over time.

.. toctree::
   :maxdepth: 2
   
   system_architecture
   devenv
   scimodules
   mysql
   macnotes
   ui_modules
   ../installation/index
   ../api/web/modindex
   ../api/modules/modindex
   lightcone
   sed
   mockimage
   telescope
   tap


=============
Galaxy Models
=============

Galaxy Models may be thought of as having three types of input properties:

#. Required: The model won't run without these properties being present
#. Optional: The model will produce additional information if these properties are present
#. Propagated: These properties are simply passed through and written to the output

SAGE doesn't follow this model yet, but it is planned for the future.

