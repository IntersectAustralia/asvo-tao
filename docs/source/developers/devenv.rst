======================
Development Enviroment
======================

The description below only covers the Web UI (Django) development enviroment.  The Science Module and Core dev. environments are TBS.

After following the initial steps as outlined in README.rst:

Edit bin/activate and add a line indicating which settings file to use by default, e.g.:

.. code-block:: sh

   $ cat >> activate <<EOF
   export DJANGO_SETTINGS_MODULE=tao.development
   export PYTHONPATH=$PYTHONPATH:$VIRTUAL_ENV/asvo-tao:$VIRTUAL_ENV/asvo-tao/web
   EOF
   $ source activate

The developer configuration settings, tao.development, assumes that MySQL is installed and a tao user and database has been created.  See <TBS>.

Initialise the database:

.. code-block:: sh

   $ manage.py syncdb
   # Answer yes to a superuser and follow-up questions
   $ manage.py migrate
   $ manage.py sync_rules

