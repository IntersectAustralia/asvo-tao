================================
Installing and Configuring MySQL
================================

This is a dump from the Developer Setup wiki page, it needs lots of love...

.. code-block:: sh

   $ unset TMPDIR
   $ mysql_install_db --verbose --user=`whoami` --basedir="$(brew --prefix mysql)" --datadir=/usr/local/var/mysql --tmpdir=/tmp
   # set a mysql user root password

Start the database::

   $ mysql.server start

Create the database and user::

   $ mysql -u root
   Welcome to the MySQL monitor.  Commands end with ; or \g.
   Your MySQL connection id is 2
   Server version: 5.5.27 Source distribution

   Copyright (c) 2000, 2011, Oracle and/or its affiliates. All rights reserved.

   Oracle is a registered trademark of Oracle Corporation and/or its
   affiliates. Other names may be trademarks of their respective
   owners.

   Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

   mysql> create user 'tao'@'localhost' identified by 'tao';
   Query OK, 0 rows affected (0.00 sec)

   mysql> grant all privileges on tao.* to 'tao'@'localhost';
   Query OK, 0 rows affected (0.00 sec)

   mysql> flush privileges;
   Query OK, 0 rows affected (0.00 sec)

   mysql> Bye

   $ mysql -u tao -p
   Enter password:
   Welcome to the MySQL monitor.  Commands end with ; or \g.
   Your MySQL connection id is 3
   Server version: 5.5.27 Source distribution

   Copyright (c) 2000, 2011, Oracle and/or its affiliates. All rights reserved.

   Oracle is a registered trademark of Oracle Corporation and/or its
   affiliates. Other names may be trademarks of their respective
   owners.

   Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

   mysql> create database tao;
   Query OK, 1 row affected (0.00 sec)

