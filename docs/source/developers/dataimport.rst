Introduction
------------


TAO Science Modules (specifically the light-cone and SED modules) expect a specific database format. TAO is required to deal with datasets with different data formats, different field names, and different data representation mechanism.

The main functionality of the data import module, which is a part of TAO admin tools, is to perform the necessary data pre-processing required to convert these datasets to the format expected from TAO science modules. 

The data import module is written in python to make it easier to understand and modify by inexperienced developers/astronomer. Since the data importing process for big datasets (e.g. Bolshoi) can take days, the code has been modified to support using MPI and direct binary data copy using psycopg2 to speed this up to less than a day. 

Input Data Format
------------------ 

The data importing process expect its input data in a single HDF5 File according to the format described in the following figure. 

.. figure:: ../_static/importingprocess_hdf5.jpg
   :alt: HDF5 Format

If such data format is not available, the developer is required to write a data conversion code to produce the described HDF5 data before using the data importing code. The array snapshot_displs are not mandatory and can safely be ignored. Other components are mandatory. These components are:

  * Cosmology group : these values present the cosmological constants used to produce the data and is provided to the science modules as a metadata. 

    * hubble: the hubble constant value used ( single value)
    * omega_l: the omega_l constant value used (single value)
    * omega_m: the omega_m contact value used (single value) 

  * galaxies: is a compound data array with each column present a field and each row present a single data record. It is an n *x* m matrix where n is the number of records and m is the number of fields. Different fields can have different data types. The importing code handle that and convert them to a suitable database datatype. 
  * snapshot_displs : It groups the data records (in galaxies) by their snapshot index. This is ignored by the data importing code.
  * snapshot_redshift: an array present the mapping between the snapshot index used and their redshift value.
  * tree_count: The data are grouped by their treeid in galaxies. The tree_count 1D array present for each tree the number of galaxies in that tree.
  * tree_displs: For each tree this 1D array contain the start index in the galaxies dataset for each tree. Both tree_count and tree_displs must be consistence.       

Data Import Process
-------------------

The following figure presents a cross-functional flowchart for the different tasks of the data importing process and how these tasks are distributed over different MPI processes. 

.. figure:: ../_static/importingprocess_CrossFunctional.jpg
   :alt: Importing Process - Cross Functional Diagram 

The details of the HDF file reading and data copying to database are presented in the following figure.

.. figure:: ../_static/importingprocess_ProcessTree.jpg
   :alt: Importing Process - Process Tree 

**The data importing process assume the following**:

  * The code assume that the data will be imported to more than one server. The mapping between table IDs and the server ID happens implicitly in a round-robin fashion.
  * The code assumes that the Number of MPI processes used >= Number of Database Servers +1 
  * Galaxies are grouped by tree id
  * Galaxies are assumed to be sorted by their local galaxies ID inside each tree (if no local galaxy id is provided)
  * The code assumes that Both tree_count and tree_displs are consistence.

The import code as shown in the cross functional diagram figure use barriers to synchronize between different processes. different sequential tasks are performed. These tasks are mainly performed by process (0) such as creating new database or adding indices to database tables.  The actual data importing process happen in the **import tree** task, which is described in more details in the second flowchart. The code support *resume* if the there was a failure in the previous importing trial. if the user select the *resume* flag to be active the code will not re-create any of the data importing helper tables or the database. It will go directly to the data importing process and continue to handle un-processed trees. Each tree is imported in a single database transaction. 

To speed-up the importing process, specially for very large trees, the code doesn't use *insert statements* to put the data from HDF5 to the database. The code utilize an important feature in postgresql and  psycopg2  which support direct copy of a binary stream of data into postgresql. In order to speed that more, the tables are generated with no index of primary keys. These indices are added later after all trees are processed. 

The process of preparing the data for such data copy process are not very easy. Postgresql expect that each record will be available in the following format:


num_fields | Field1_length | Field1  | Field2_length | Field2 ........... Fieldn_length | Fieldn| 

The importing code prepare this format in a numpy array for all the fields in the HDF5 file and the computed fields. The code automatically handle the datatype mapping for different datatypes. 

See `COPY <http://www.postgresql.org/docs/9.2/static/sql-copy.html>`_ (Binary Format Section) For further details.


Settings for the data importing module
--------------------------------------
.. figure:: ../_static/import_setting1.jpg
   :alt: import setting(a)

.. figure:: ../_static/import_setting2.jpg
   :alt: import setting(b)