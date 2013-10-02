SED - distance modulus test
===========================

SED distance modulus test is for low redshift galaxies (z << 0.5). The goal of 
the test is to check if the distance that comes from difference between absolute
and apparent magnitude is corresponding to the actual distance in the catalogue.

The code includes K-correction calculator downloaded from:
    http://kcor.sai.msu.ru/calc_kcor.py
    Reference:
    http://adsabs.harvard.edu/abs/2012MNRAS.419.1727C

and custom developed redshift calculator:
    calc_z2d.py


Catalogue requirements
----------------------

Catalogues must be in TAO CSV format, using ", " as a delimiter.

Tested catalogues must include:
    distance
    redshift_cosmological
    johnson/rfilter.dati_apparent
    johnson/johnson_b.dati_absolute
    johnson/johnson_b.dati_apparent

If field names or delimiter change then test-dm.py must be modified accordingly.


Usage
-----

Run from command line:
    python test-dm.py <input catalogue>


Results
-------

The script will output following columns:
z   d(z)   d(TAO)   d(DM)   diff %

where:
    z      - redshift from TAO catalogue
    d(z)   - distance calculated from the redshift
    d(TAO) - distance from the TAO catalogue
    d(DM)  - distance calculated from distance modulus
    diff % - difference between distances d(TAO) and d(DM) in [%]


Interpreting the results
------------------------

The difference between d(TAO) and d(DM) should be approaching to 0. This value
can grow with higher redshift values.

