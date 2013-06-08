======================
Development Enviroment
======================

After following the initial steps as outlined in README.rst:

Edit bin/activate and add a line indicating which settings file to use by default, e.g.:

.. code-block:: sh

   $ cat >> activate <<EOF
   export DJANGO_SETTINGS_MODULE=development
   EOF
   $ source activate

If the database needs to be initialised:

.. code-block:: sh

   $ manage.py syncdb
   # Answer yes to a superuser and follow-up questions
   $ manage.py migrate
   $ manage.py sync_rules

