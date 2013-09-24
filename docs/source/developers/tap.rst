TAP Server
==========

TAP Protocol
------------

The table access protocol `VO Table Access Protocol (TAP) <http://www.ivoa.net/documents/TAP/>`_ is an `International  Virtual  Observatory  Alliance (IVAO) <http://www.ivoa.net/>`_ standard protocol for providing access to astronomical data.

Synchronous access
------------------

There is no direct access to the database from the client side. Synchronous data querying in the TAP Server is emulated by the web application via regular workflow job submission and serving data to the client upon the job completion. 

Asynchronous access
-------------------

Communication between client application and the TAP Server is designed to follow `Universal Worker Service Pattern (UWS) <http://www.ivoa.net/documents/UWS/20100210/PR-UWS-1.0-20100210.html>`_.
Implemented services:

- capabilities
- availability 
- tables
- query
- sync
- async
- job
- phase
- quote
- termination
- destruction
- owner
- error
- params
- results
- result

.. figure:: ../_static/uws_sequence_diagram.png
   :alt: UWS Sequence Diagram

SQL/ADQL Queries
----------------

Current TAO implementation supports SQL/ADQL only partially. Allowed SQL functionality is:

- Select statement with the list of requested data fields. No mathematical operations are allowed.
- Limit SQL clause or TOP MSSQL statement.
- Where SQL clause with boolean conditions. No mathematical operations are allowed.

Authentication
--------------

TAP Server application using HTTP Basic Authentication. To allow Apache HTTP server to pass authetification headers following line needs to be added to .htacces file:

.. code-block:: sh

   RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

