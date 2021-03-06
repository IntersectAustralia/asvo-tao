TAO Science Modules Web Interface
=================================

Introduction
------------

This document describes how the user interface to TAO science modules is structured in the web component and therefore how a new science module can be integrated into the TAO system.

It is expected the reader will be familiar with development concepts for the web, particularly the Python programming language and the Django framework, although every effort has been made to make the extension process as easy as possible.

A companion document "TAO science modules" describes the work required to extend the TAO system in the backend, where the computational framework resides. The reader should also get familiar with that.

UI Modules Overview
-------------------

A UI module is in charge of capturing and displaying specification parameters that will configure a particular execution of one or multiple backend modules. Putting together the specification provided by each module and submitting it to the backend is the job of 
the TAO web interface.

Modules in TAO may have interdependencies but the system is designed so that modules are dealt with in isolation. So, ideally, modules in the backend should be designed so they are as independent as possible - from a specification perspective. Interdependencies in the data input, when necessary, are to be implemented through JavaScript. Having more or less independent module specifications makes the overall design simpler to implement and use from a developer’s perspective.

It is not possible a priori to anticipate all UI needs that will be required by the addition of a module. However, there is core infrastructure that can be used to facilitate the creation of UI forms for new modules, on top of what the Django framework already provides.

TAO UI modules have been designed using the concept of a Django application. It means that the web application is composed of quasi-independent modules, or "applications" in Django parlance, that are integrated at build time. A new science module is effectively a new Django application.

However, to keep things simple, the TAO web interface does not use the full power of a Django application and just uses them to provide code isolation, pluggable templates and module specific database storage, if required. For example, application-defined URL spaces are not necessary.

A UI module is defined as a combination of some Python, HTML, CSS and JavaScript, in a way somehow similar to how a full web UI is defined. This makes the approach quite flexible for developers, as opposed to a more declarative approach. This was a conscious decision: a completely declarative UI specification was not implemented because this approach would have been very constrained, as it is usually; and on the other hand requires lot more effort to implement, document and work with.

The TAO system, at the time of writing, comes with two defined TAO UI modules (Light Cone and SED) which the developer is encouraged to explore to learn. The source code for both, the TAO system and the TAO UI modules is available on github, see References at the end of this document.

The rest of the document is organized as follows. "Form lifecycle" provides an account of the lifecycle of a UI module inside the TAO web interface and its data flow. "How to add a new module" presents a more detailed picture of what a UI module looks like and how integration happens for a basic module. "XML processing" has a few specific aspects to consider when writing the XML specification of a module. "Complex modules" mentions how to use the power of Django to write more complex modules that require database integration. "Conclusions" draws some final remarks about the modular UI capability of the TAO system.

Form Lifecycle
--------------

As stated above, UI modules are responsible for capturing and displaying specification parameters for a job. Central to a UI module is a ``Form`` class. In existing modules it is inherited from ``BetterForm`` (from ``django-form-utils``; details of this to be explained in next chapter), although any implementation of Django form can be used. The Form class is instantiated and used at different moments of the user’s interaction with the TAO web component as outlined below:

Creating a Job
^^^^^^^^^^^^^^

To create a new job, the researcher goes through the following steps:

1. User visits new job page
2. The new job page is displayed by the web application
3. The form is filled with specification values for each module by the user
4. If the all the required fields are supplied and valid on the client-side, the submit button is enabled, otherwise it informs the user of errors
5. Once the form is valid, the user submits the form
6. The web application receives the form data and validates it
7. If ok, then a job is created with the specification values
8. Otherwise the job form is re-displayed with errors.

From a UI module developer’s perspective, steps 2 (form display), 4 and 6 (form validation), 7 (XML generation) and 8 (form display) are the ones relevant for implementation. The following sections outline how the ``Form`` object is used in each instance, so an appropriate implementation can be written.

Form Display
""""""""""""

Displaying a form involves two actions on the server side:

1. The module’s ``Form`` object is instantiated with empty parameters
2. The module’s ``edit.html`` template is rendered inside the job-edit page

Developer’s main concerns here are implementing default values in the constructor, defining the fields in the form, and displaying the fields properly in the template. When re-displaying the form after validation fails, the only difference is that the ``Form`` object is instantiated with values from the request (see next), the template used is the same.

On the client side:

1. The forms fields possible values are populated (e.g. ``<option>`` s in a ``<select>``)

Form Validation
"""""""""""""""

On the client side, JavaScript validation if performed that:

1. Checks that required fields are present
2. That fields values are valid

Only then is the submit button enabled. Here the developers main concern is to ensure that the knockout observables have the appropriate validation extensions. On the server side, when data is received two steps also occur in this case:

1. The ``request.POST`` data is passed as parameter to instantiate the module’s ``Form`` object,
2. Then validation is executed

The developer’s main concern here is to grab the corresponding values from the request. This should of course match whatever is displayed in the template. Much of the work, however, can be handled by the ``django-form-utils`` if the developer uses it, and the he/she can implement custom validation by extending ``Form.clean`` instance method. Upon errors, the same instance of the ``Form`` object (created with values from the request), gets passed to the template for re-display (see previous.)

XML Generation
""""""""""""""

If the validation succeeds, the very same ``Form`` instance is used to generate the XML fragment for the job specification and saved to the database. It is assumed that the generated XML follows the guidelines where a module’s XML is distinguished from others by module-id. This will be explained in greater detail in "XML processing".

UI Module JavaScript Framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section describes the framework used to manage the JavaScript which accompanies a UI module, and how to implement the interface when creating additional modules. In addition to the commonly used jQuery library, the interface relies heavily on the `Knockout.js <http://knockoutjs.com/>`_ library and it is recommended that you familiarise yourself with its basic concepts before delving into this section.

UI Module Lifecycle on the Client
"""""""""""""""""""""""""""""""""

The HTML form elements sent from the server start off empty, and the fields defaults and possible values are populated via JavaScript.

There are two important JavaScript variables sent from the server, ``TaoMetadata`` and ``TaoJob``. ``TaoMetadata`` contains all the database options for creating a job, ``TaoJob`` contains parameter values to initialise the fields with. ``TaoJob`` will be empty if the user creates a new job, but will be populated if a user uploads a parameter file or selects a preset.

Initialisation
**************

Each UI Mmodule has its own JavaScript file located deep in its static subfolder, for the SED module the file is located in ``ui/sed/taoui_sed/static/js/taoui_sed/sed.js``. These modules conform to a simple interface that allows ``catalogue.js`` to control the initialisation of modules, below is a snippet of ``light_cone.js``::

    // Setup the namespace in case it hasn't been created
    var catalogue = catalogue || {};
    catalogue.module_defs = catalogue.module_defs || {};

    // Module definition passing the current jQuery object to the constructor
    catalogue.module_defs.light_cone = function ($) {

        // Knockout ViewModel
        var vm = {}

        this.init_model = function(init_params) {
            // initialise module Knockout ViewModel

            return vm;
        }        

    }

Here the ``init_params`` is a reference to ``TaoJob``, which the module can use to set the initial module parameters. Once each module has created its view model, ``catalogue.js`` calls knockout's ``applyBindings()`` method.

Validation
**********

Modules are also responsible for both client and server side validtion. On the client side, ``catalogue.js`` contains a number of validators in the form of knockout extensions (located in the ``catalogue.validators`` namespace), but you can add more as required. Below is an example of a field from the Light-Cone module being initialised with validators::

    param = job['light_cone-redshift_min'];
    vm.redshift_min = ko.observable(param ? param : null)
        .extend({required: function(){return vm.catalogue_geometry().id == 'light-cone'}})
        .extend({only_if: function(){return vm.catalogue_geometry().id == 'light-cone'}})
        .extend({validate: catalogue.validators.is_float})
        .extend({validate: catalogue.validators.geq(0)});

The validators prevent invalid forms from being submitted by disabling the submit button, and communicate to the user where the errors lie.

Viewing a Previously Submitted Job
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To view an existing job, the researcher goes through the following steps:

1. User goes to the Jobs list
2. The job list page shows each job with a view link
3. User clicks the view link on a job
4. The job view page is displayed by the web application

From a UI module developer’s perspective, the only step that matters is 4, job display. This implies that, at least for now, a UI module cannot participate in the list page proving a custom overview for a submitted job.

Job Display
^^^^^^^^^^^

Displaying a stored job involves several actions in the web application:

1. The full job description is grabbed from the database in XML format.
2. Each "module" element is processed in turn: based on the module-id, the corresponding ``Form`` module object gets created using the ``Form.from_xml`` class method with the full XML document as parameter.
3. This object is converted to JSON object and assigned to the ``TaoJob variable``
4. The module’s ``view.html`` template is rendered inside the job-view page with the corresponding ``Form`` object.
5. JavaScript on the client initialises field values using the ``TaoJob`` object

The developer’s main concerns here are implementing the ``from_xml`` class method with the XML document as parameter, and displaying the fields properly in the view template. In terms of JavaScript, the mechanism for viewing a job is the same as loading a parameter file.

Adding a New Module
-------------------

UI modules are Django applications. The following section briefly outline the steps to create a UI module and link it to the TAO web component. Next, the following sections come with some notes for UI module developers that further explain the API.

Basic Steps
^^^^^^^^^^^

1. Create New Module Source
"""""""""""""""""""""""""""

Create a new branch in repository (asvo-tao-ui-modules). The recommended way is to create an orphan branch, like ``git checkout --orphan light-cone``. Notes: you need git version >= 1.7.2 to do this; and, you can use other repository if compatible with buildout.

To avoid packages split across directories, each module lives in its own top-level package, which has to be named ``taoui_<module>``. Templates also have to be defined in their own uniquely named directory inside templates to avoid conflicts with other modules.

The structure of a UI module should be like (for a module called ``dark_cone``)::

    taoui_dark_cone/
        __init__.py
        admin.py
        forms.py
        models.py
        templates/
            taoui_dark_cone/
                edit.html
                view.html
            assets/
                taoui_dark_cone/
                    special.js
        static/
            taoui_dark_cone/
                icon.png
                style.css
                main.js

``forms.py`` must define a ``Form`` class. It is recommended to inherit from ``BetterForm`` (``django-form-utils``), although this is not compulsory as long as the API is respected. The recommend library, ``django-forms-util``, has a number of field types and helpers which facilitates the creation of web forms. Note that Django’s ``Form`` API has the concept of 'prefix' to provide namespacing for fields. We strongly recommend to use this feature (see existing modules for an example.) The reader should read its documentation as mentioned at the end, in "References"

``models.py`` can contain extensions to the web component database (see corresponding chapter.) It is required by the Django framework, so even if there are no extensions, an empty file needs to be there.

``admin.py`` is optional and used by the admin utility. See "Complex modules" to further explanation.

The ``templates`` directory gets added by the Django framework to the template search path. To avoid name conflicts, modules should place their templates underneath in a uniquely named directory. The names of the editing and viewing templates are not fixed: the ``Form`` object is responsible to point to them, including the relative path (i.e. subdirectory).

The ``assets`` subdirectory can be used to render parametrized JavaScript, a facility provided by TAO web via its ``js-asset`` tag. As with templates, one needs to provide a custom directory to avoid name conflicts.

The ``static`` directory gets added by the Django framework to the static search path. To avoid name conflicts, modules should place their static assets underneath a uniquely named directory. Assets are then referred to from the template by name using that subdirectory name.

The reader is strongly encouraged to inspect the code of already included UI modules before creating his/her own.

2. Configure New UI Module in TAO Web
"""""""""""""""""""""""""""""""""""""

This is done in two steps. First, one needs to modify buildout.cfg and include the pointers to the new module’s source repository, and ``settings.py`` needs to list the newly included module in the ``MODULES`` variable, like::

    MODULES = ('light_cone', 'sed', 'dark_cone', ) 

Once this is done, one just need to run ``$ bin/buildout`` to get the module source downloaded and the Python path configured in ``bin/django``.

That’s it. If the Django TAO web was already built (see development documentation), it is ready to run again. Type ``$ bin/django runserver`` to test it locally. Note that the order in which modules are listed in the ``MODULES`` variable is the order in which they are processed, rendered and displayed to the user.

Form API
^^^^^^^^

The Python ``Form`` class needs to implement the following methods:

* Constructor ``(__init__)`` with optional ``dict`` argument: used to populate the fields prior to rendering or validation.
* ``is_valid``: called by TAO web to trigger validation.
* ``clean``: implemented by ``BetterForm``; can be overridden by ``Form`` subclass. Called as part of the ``is_valid`` implementation.
* ``to_xml``: instance method that adds XML elements to a provided XML document.
* ``from_xml``: class method that receives a ``<module .../>`` fragment to instantiate the ``Form`` object from it.
* ``EDIT_TEMPLATE``: name of the editing template, e.g. ``taoui_dark_code/edit.html``
* ``VIEW_TEMPLATE``: name of the viewing template, e.g. ``taoui_dark_code/view.html``

The module's JavaScript also needs to implement:

* ``init_model``: function called by ``catalogue.js`` to create tge module's view model before knockout's bindings are applied.

For more details see the section "UI Module JavaScript Framework".

Integrating with TAO Web
^^^^^^^^^^^^^^^^^^^^^^^^

Both the form code and the XML code can import any part of the TAO base application and use them as required. For example, to query the model objects, the developer can import models from the tao package and use ``models.GalaxyModel.objects.all()`` to load the ``GalaxyModel`` instances.

You will see an example of this in the ``light_cone`` module. When the database logic becomes complex, it is highly recommended to put that logic in a separate Python script and refer to it from the new form.

On the other hand, ones need to be aware that a module’s template is rendered as part of an existing html. It is worth noticing that TAO web uses Twitter’s bootstrap CSS styles and the reader is encouraged to see existing modules as examples that play nicely with the overall page design.

In addition, each module can define its own JavaScript and conflicts may arise. In this regard inspection of existing modules and their JavaScript should be done before integrating new JavaScript code to the editing page. TAO web includes jQuery as JavaScript library by default which can be used by developers.

Finally, TAO web extends native Django facilities providing:

* ``ChoiceFieldWithOtherAttrs``: custom field extension to ChoiceField that injects additional attributes in the <option../> element.
* ``js-asset``: a custom template tag to render a JavaScript inclusion as a django template.
* workflow’s ``param`` and ``add_parameters``: helper methods to generate XML ``<param.../>`` elements.


XML Processing
--------------

As mentioned "Form lifecycle", XML processing is necessary to store a job specification into the database and also to display a job already stored in the database. The particulars of the XML schema used are not in scope for this document and described elsewhere.

In that chapter, XML generation was explained: XML is generated by the ``Form`` object via its ``to_xml`` method that receives a XML parent node and injects new elements in there. TAO web uses the ``lxml`` Python library, so module creators should follow that.

There is an existing mismatch between UI modules and ``<module ../>`` elements, in which some UI modules generate multiple ``<module ../>`` elements. This highlights the flexibility of the approach, although developers need to be careful to generate elements that can be distinguished somehow from other modules.

The generated XML document is then stored in the database and retrieved by the web-services API offered to the job managing client that interacts with HPC facilities. It is important to keep the XML in synch with that client (``science_modules`` directory in the ``asvo-tao`` project). Please refer to the Science Modules documentation.

Finally, when it comes to displaying an stored job in the TAO web component, as said before, the ``from_xml`` class method is called *with the whole XML document*, which should populate the internal fields so they get displayed properly in the template. The reason it is called with the full document tree is that a UI module can actually create multiple elements in the document tree and there needs the whole document to be able to retrieve the element relevant to it. As just said above, developers need to be aware of this to avoid clashing with other module’s elements.

Complex Modules
---------------

TAO web comes with a number of defined concepts: ``simulation``, ``dataset``, ``galaxy_model``, etc. A UI module developer can make use of those, as some of the existing modules do. However, it may happen that a new module requires new options that are better described and stored in a database table. This chapter provides an overview of the steps involved in creating such a module.

Existing Models
^^^^^^^^^^^^^^^

In django parlance, a model is a class mapped to a database (usually a single table.) The database for TAO web (known as MasterDB) contains mappings for ``GalaxyModel``, ``Simulation``, ``DataSet``, ``Snapshot``, ``DataSetParameter``, and ``StellarModel``. The ``GalaxyModel``, ``Simulation``, and ``StellarModel`` are metadata classes. Their information is displayed at the side of the form when they are selected. The ``DataSet``, and its associated related models ``Snapshot`` and ``DataSetParameter`` contain options.

As mentioned in "Integrating with TAO web", one can simply import those classes into a form and start using Django’s database mapping features. If the ones above are not sufficient, the following sections describe how to add new models.

Adding Tables to the Database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The TAO web component is a South-enabled project. This means it uses South (see references) to manage the evolution of the database schema. To create new tables, it is strongly recommended that you take advantage of Django’s models and South. To do so, there are a few things to be done:

1. Create new models in ``models.py`` inside your UI module. You can create many model classes inside ``models.py``
2. Create a migration - ``bin/django schemamigration --auto <module>``
3. Run the migration - ``bin/django migrate <module>``

South will scan your ``<module>`` for newly created models and create and apply the database migrations accordingly. Note that those migrations will become part of the main TAO web project! For more details on how to migrate the database and use your new model(s), please see references.

Using New Models
^^^^^^^^^^^^^^^^

Newly created models in your UI module can be imported in the ``Form`` definition as any other module in the TAO web project. As said above, the reader should be familiar with Django’s models API to do this.

Django’s Admin Interface
^^^^^^^^^^^^^^^^^^^^^^^^

As final remark, if Django’s native admin interface is suitable for editing data in the added tables, one only needs to add the following in the ``admin.py`` script inside the module.::

    from django.contrib import admin
    from taoui_<module>.models import <Model1>, <Model2>, ...

    for model in (<Model1>, <Model2>, ...)
        admin.site.register(model)

where ``<Model_>`` are the actual mapping classes defined in your code, and ``<module>`` is your module name as discussed before. See the references for further customization.
