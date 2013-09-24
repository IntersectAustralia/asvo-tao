TAP Server
==========

TAO TAP Server follows standards of the `International Virtual  Observatory  Alliance (IVAO) <http://www.ivoa.net/>`_. Results of the data querying are served to client in `VOTable format <http://www.ivoa.net/documents/VOTable/>`_.

* To use TAO TAP Server user must be registered on the TAO web site:
https://tao.asvo.org.au/tao/accounts/register/

* TAP entry point URL for TAP client applications, like `TOPCAT <http://www.star.bris.ac.uk/~mbt/topcat/>`_:
https://tao.asvo.org.au/tao/tap

* TAO TAP Server supports only basic ADQL/SQL functionality. Current restrictions include:

  * Mathematical, statistical or string operations are not supported. 
  * Table "JOIN" or "UNION" are not supported.
  * Offset/paging is not supported. Limit can be applied to number of records returned by using MSSQL "TOP" statement, or SQL "LIMIT" statement, or by adding "MAXREC" value to the request POST data ("Max Rows" in the TOPCAT interface). 
  * Sorting, aggregate and grouping functions are not supported.

* There are synchronous and asynchronous data querying available in the TAO TAP Server. But it is recommended to use asynchronous querying as it doesn't need to keep the connection open for a long period of time and therefore is more stable.
