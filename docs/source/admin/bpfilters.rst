BandPass Filters
================

BandPass Filters are simple text files containing a header entry with the number of records, followed by the records themselves.  Each record consists of two space separated fields: the wavelength and transmission index, e.g.::

   58
   13000.00      0.0000000E+00
   13150.00      0.0000000E+00
   14180.00      0.0000000E+00
   14400.00      5.0000002E-04
   14620.00      2.7999999E-03
   14780.00      8.1000002E-03
   14930.00      8.7099999E-02
   15150.00      0.4382000    
   15280.00      0.6864000    
   15390.00      0.8181000    
   ...

Note that duplicate entries, i.e. with the same wavelength, are not allowed and will cause an error when running a job that uses the associated bandpass filter.

The filters may be placed in a hierarchical directory structure to avoid filename clashes between sources, but must have a unique id within the Master DB.

Loading Bandpass Filter Metadata
--------------------------------

To import the bandpass filter metadata, create a CSV file with the following columns:

#. Filename (relative)
#. Label
#. Description

E.g.::

   "2MASS/Hband_2mass.dati",   "2MASS H", "2 Micron All Sky Survey (2MASS) H"
   "ACS/f435w.WFC1.dati", "HST/ACS/WFC1 B", "Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 1 (HST/ACS, WFC1), B band (F435W)"
   "ACS/f435w.WFC2.dati",  "HST/ACS/WFC2 B", "Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 2 (HST/ACS, WFC2), B band (F435W)"
   "CFHTLS/uMega.dati",  "CFHTLS Megacam u*", "Canada France Hawaii Telescope (CFHTLS/Megacam), u* band"
   "CFHTLS/gMega.dati",  "CFHTLS Megacam g' ", "Canada France Hawaii Telescope (CFHTLS/Megacam), g' band"
   "CFHTLS/rMega.dati",  "CFHTLS Megacam r' ","Canada France Hawaii Telescope (CFHTLS/Megacam), r' band"
   ...

From the root directory where the filters are located, import the metadata by running::

   $ manage.py add_bpfilters <metadata.csv> </path/to/asvo-tao/docs/>

This will:

#. Generate spectra of each of the filters and update the documentation source.
#. Update the Master DB BandPassFilter table with the metadata provided in the CSV file and links to the spectra.

It is also possible to just add the core metadata to the Master DB without generating spectra using the ``--no-doco`` option, and to scan the filters for duplicate wavelengths with the ``--check-dups`` option.

add_bpfilters adds new metadata and updates existing metadata.  If any filters ahave been deleted it will be necessary to manually remove them from the Master DB.  This can be done using the Django shell::

   $ manage.py shell_plus
   BandPassFilter.objects.all().delete()

For more information::

   $ manage.py add_bpfilters --doc


Configuring BandPass Filters for the SED Module
-----------------------------------------------

To be supplied by Amr...

