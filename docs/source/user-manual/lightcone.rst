Light Cone Module
=================

The light cone module facilitates the selection of a subset of the simulated universe in one of two geometries:

#. Box: Returns a single snapshot (redshift) of the simulated universe.
#. Cone: Maps the geometry of the simulated data cube on to the observer cone

Common Parameters
-----------------

Dark Matter Simulation and Galaxy Model
   Together the Dark Matter Simulation and Galaxy Model select the dataset.



Light-Cone Geometry
-------------------

Right Ascension, Declination and Redshift

   Together define the dimensions of the light cone.

Unique / Random

   If the dimensions of the light-cone exceed the dimensions of the simulation the simulated space is simply repeated out to the required dimensions.

   Selecting Unique ensures that no volume from the original simulation space is used multiple times in the resulting light-cone.

   Selecting Random allows the universe to be expanded indefintely, with the original cube randomly rotated each time it is repeated to minimise any patterns appearing through repitition.

