TAP Server
==========

TAP Protocol
------------

TAP server returns job results and answers API calls using table access protocol: `VO Table Access Protocol (TAP) <http://www.ivoa.net/documents/TAP/>`_ is an `International  Virtual  Observatory  Alliance (IVAO) <http://www.ivoa.net/>`_ standard protocol for providing access to astronomical data.


TAP Server
----------

Communication between client application and the TAP Server is designed to follow `Universal Worker Service Pattern (UWS) <http://www.ivoa.net/documents/UWS/20100210/PR-UWS-1.0-20100210.html>`_.
Public interfaces available at the TAP server are:

- https://tao.asvo.org.au/tao/tap/capabilities - returns XML schema with the server capabilities;
- https://tao.asvo.org.au/tao/tap/availability - returns server status;
- https://tao.asvo.org.au/tao/tap/tables       - returns metadata of the available for querying datasets.


Authentication
--------------

TAP Server application uses HTTP Basic Authentication. To allow Apache HTTP server to pass authentication headers following line needs to be added to .htacces file:

.. code-block:: sh

   RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]


Synchronous job submission
--------------------------

There is no direct access to the database from the client side. Synchronous data querying in the TAP Server is emulated by the web application via the workflow job submission, regular poling the job status and finally serving the data to the client upon the job completion. 

Synchronous jobs must be submitted to: 

https://tao.asvo.org.au/tao/tap/sync 

with POST parameters:
  * QUERY - containing SQL/ADQL query.
  * REQUEST - must be equal to "doQuery", otherwise submission call is ignored.


Asynchronous jobs
-----------------

Asynchronous job can be submitted to:

https://tao.asvo.org.au/tao/tap/async 

with the same set of POST parameters: QUERY="<query>" and REQUEST="doQuery".

After the job is submitted, the client is redirected to the newly created job interface: 

`https://tao.asvo.org.au/tao/tap/async/<job_id>`

which contains job id in the URL, and returns job status and parameters in XML format defined by the IVOA UWS schema: http://www.ivoa.net/xml/UWS/v1.0

The TAP server supports job interfaces defined by the IVAO standards: 

  * `https://tao.asvo.org.au/tao/tap/async/<job_id>/phase`
  * `https://tao.asvo.org.au/tao/tap/async/<job_id>/quote`
  * `https://tao.asvo.org.au/tao/tap/async/<job_id>/executionduration`
  * `https://tao.asvo.org.au/tao/tap/async/<job_id>/destruction`
  * `https://tao.asvo.org.au/tao/tap/async/<job_id>/results`
  * `https://tao.asvo.org.au/tao/tap/async/<job_id>/error`

Asynchronous job call sequence is shown on the diagram:

.. figure:: ../_static/uws_sequence_diagram.png
   :alt: UWS Sequence Diagram
   

SQL/ADQL Queries
----------------

Current TAO implementation supports SQL/ADQL partially. Allowed SQL functionality is:

- Select statement with the list of requested data fields. No mathematical operations are allowed.
- Limit SQL clause or TOP MSSQL statement.
- Where SQL clause with boolean conditions. No mathematical operations are allowed.

