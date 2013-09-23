TAO Hardware and Database Architecture
======================================
.. figure:: ../_static/mainsystem.png
   :alt: Main system hardware design


Design Assumptions
------------------

- In order to support `VO Table Access Protocol (TAP) <http://www.ivoa.net/documents/TAP/>`_, the ability to support executing direct SQL query to the database (the simulation data) is a mandatory requirment. This limit the ability to use No-SQL Databases and HADOOP-like processing architecture.
- Efficient handling of large datasets is the main challenge for the TAO project. In this context, the ability to query and access the underlying datasets is the system’s main performance bottleneck.
- Using a commercial version of a distributed Relational Database Management System (RDBMS) will limit further adoptability of the system in an open source enviroment and add a significant burden on the system main budget.


Design Decisions
----------------

- Using a distributed (cluster) database solution is preferred over the single node DBMS. Using cluster DBMS will speed-up different data access processes, and support better system scalability to more and bigger datasets.
- The current hardware architecture is partitioned into three main servers and the `SwinSTAR Supercomputer <http://astronomy.swin.edu.au/supercomputing/green2/>`_ with the following specifications:
  
  * One low-end Web-Server (Node A in figure 1)
  * Two identical medium class application/database-servers (Node B and C in figure 1)
  
The functionality and details of these nodes will be discussed in details in the next section.
