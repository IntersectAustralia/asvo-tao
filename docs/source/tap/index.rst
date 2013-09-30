TAP Server
==========

TAO TAP Server follows standards of the `International Virtual  Observatory  Alliance (IVAO) <http://www.ivoa.net/>`_. Results of the data querying are served to client in `VOTable format <http://www.ivoa.net/documents/VOTable/>`_.

User access
-----------

To use TAO TAP Server the user must be registered and approved on the TAO web site:
https://tao.asvo.org.au/tao/accounts/register/

Application entry point
-----------------------

TAP entry point URL for TAP client applications, like `TOPCAT <http://www.star.bris.ac.uk/~mbt/topcat/>`_ is:

`https://tao.asvo.org.au/tao/tap <https://tao.asvo.org.au/tao/tap>`_

Job submission
--------------

There are synchronous and asynchronous data querying modes are available in the TAO TAP Server. It is recommended to use asynchronous querying as it doesn't need to keep the connection open for a long period of time and therefore is more stable.

To submit a job please follow instructions provided with the client application software. Sample instructions how to use `TOPCAT can be found here <http://www.star.bris.ac.uk/~mbt/topcat/sun253/index.html>`_:

1. `Enter the TAP service entry URL <http://www.star.bris.ac.uk/~mbt/topcat/sun253/TapTableLoadDialog_service.html>`_
2. `Enter a query <http://www.star.bris.ac.uk/~mbt/topcat/sun253/TapTableLoadDialog_query.html>`_ 
3. `Monitor running jobs <http://www.star.bris.ac.uk/~mbt/topcat/sun253/TapTableLoadDialog_jobs.html>`_
4. `Access completed jobs <http://www.star.bris.ac.uk/~mbt/topcat/sun253/TapTableLoadDialog_resume.html>`_

Once the job is completed it will be loaded in the TAP client application automatically. 

Job access
----------

If connection between the client application and the TAP server is closed it is possible to re-connect with the job via the asynchronous interface, regardless if the job was submitted via synchronous or asynchronous interface. The asynchronous job URL is based on the job id:

`https://tao.asvo.org.au/tao/tap/async/<job_id>`.

Example: if the job id is 12345, then asynchronous job access link is `https://tao.asvo.org.au/tao/tap/async/12345`.

Once client application loaded the job link, it can query the job status. If the job is completed the results can be downloaded at any time, until the job is deleted by the user via the jobs history interface in the TAO web application.

Additional information and limitations of the job controlling on the TAO TAP server:
  * Job starts automatically when query is submitted to the TAP server along with the POST data REQUEST parameter with the value "doQuery" (automatically included in the TOPCAT). Submission of the POST data PHASE=RUN to the job interface is not required.
  * Abort and delete calls will abort the running job.
  * Asynchronous job pause/resume functionality is not supported.
  
Querying
--------

TAO TAP Server supports only basic ADQL/SQL functionality. Current restrictions include:

  * Mathematical, statistical or string operations are not supported. 
  * Table "JOIN" or "UNION" are not supported.
  * Offset/paging is not supported. Limit can be applied to number of records returned by using MSSQL "TOP" statement, or SQL "LIMIT" statement, or by adding "MAXREC" value to the request POST data ("Max Rows" in the TOPCAT interface). 
  * Sorting, aggregate and grouping functions are not supported.
  