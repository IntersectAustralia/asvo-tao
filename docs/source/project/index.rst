Introduction
************

The Theoretical Astrophysical Observatory (TAO) will house queryable data from
multiple popular cosmological simulations (currently the Millennium Simulation, 
with Bolshoi Simulation and GiggleZ Simulation planned) and galaxy formation models 
(currently Croton et al. 2006 (SAGE), with Somerville et al. 2008 and Benson 2010 planned) in a 
database that is optimised for rapid access. Query results can be funnelled 
through additional "modules" (described below) and sent to a local supercomputer 
for further processing and manipulation. All of this is accessible via the cloud 
through a browser for access anywhere in the world by the astronomical community 
using a simple wizard based UI, in particular: no knowledge of SQL is required.

Modules
-------

Light-Cone Module
^^^^^^^^^^^^^^^^^

This module re-maps the geometry of the simulated data cube on to the observer cone. Cone parameters are configurable and popular survey geometries will be available as presets.

Science: Mock light-cones are commonly used in survey science to test for systematics and biases in the data, as well as to explore science questions of interest in a more realistic setting. TAO will enable users to generate identically produced cones that are sourced from different simulations and models, something that has never been done before.

Spectral Energy Distribution (SED) Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This module takes the simulated data and offers a choice of different popular SED models to apply in post-processing. The SED Module is required by the Light-Cone Module to produce apparent magnitudes, but can be independently applied to any data in the theory observatory (e.g. the original data cube).

Science: SED post-processing will vastly expand the wavelength coverage of all simulated galaxy data in the database regardless of its original state. This will open up TAO to a wide range of the community, from radio to optical to IR. It will additionally provide a way to compare the predictions of different SED models and explore the theoretical uncertainty between them.

Futures
-------

TAO has been designed to be extensible so that additional modules can be built and easily inserted into the data chain as needs evolve in the future (e.g. a module to perform lensing on the simulated data).

We are planning to add two more modules as part of the current project:

#. Mock Image Generation Module
#. Telescope Module

For additional information about these modules, please see below.

We also have a number of enhancements planned as part of the current project:

* Job Quota Management.  This will calculate a maximum execution time for each job ensuring that the system is not blocked by jobs that are too large.  If you would like to run a job that exceeds your quota, please submit a support request.
* Disk Quota Management.  The ability to delete mock catalogues that are no longer required will be added.


Mock Image Generation Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This module takes the output of both the Light- Cone Module and SED Module and produces user defined mock images. Image parameters are configurable (e.g. area on the sky, depth, filter).

Mock images can be used to test source finding algorithms and to test the accuracy of galaxy environment measurements (to name but two examples).

Telescope Simulator Module
^^^^^^^^^^^^^^^^^^^^^^^^^^

This module extends the functionality of the Light- Cone and SED Modules. It further filters the mock data to more closely mimc that expected from a particular telescope, for example by adding instrument noise. We will initially focus on the most popular telescopes available to Australian astronomers, however more can be added in the future.

Science: By itself the Telescope Simulator Module can be used to generate different mock realisations of a proposed galaxy survey performed with a particular telescope. Combined with the Mock Image Generation Module, a user can simulate the expected imaging one would expect the telescope to produce.

Additional Datasets
^^^^^^^^^^^^^^^^^^^

TAO currently only contains the :ref:`Millennium <Millennium>` / :ref:`SAGE <SAGE>` dataset.  We currently plan 
to add the following datasets:

* :ref:`Bolshoi <Bolshoi>` / :ref:`SAGE <SAGE>`
* :ref:`Millennium <Millennium>` / :ref:`Galacticus <Galacticus>`
* :ref:`Bolshoi <Bolshoi>` / :ref:`Galacticus <Galacticus>`


Transformational Science
------------------------

Numerical astrophysics is emerging as an integral component of upcoming next generation survey programs, and the simulations generated as part of these programs will need a home. The Theoretical Astrophysical Observatory provides this home.

Expertise
---------

The TAO project team combines expertise in N-body and hydrodynamic simulations with all varieties of galaxy formation modelling in a high performance computing environment.

The project enables investigation into a wide range of interesting astrophysical phenomena, including (1) cosmology, dark matter and dark energy, (2) galaxy assembly, evolution and interactions, (3) supermassive black holes and quasars, and (4) large-scale structure, voids and environmental effects.


