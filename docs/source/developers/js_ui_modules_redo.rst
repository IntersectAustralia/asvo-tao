Introduction

This section describes the framework used to manage the JavaScript which accompanies a UI module, and how to implement the interface when creating additional modules. In addition to the commonly used jQuery library, the interface relies heavily on the `Knockout.js <http://knockoutjs.com/>_` library and it is recommended that you familiarise yourself with its concepts before delving into this section.

UI Module Lifecycle

The html form elements sent from the server start off empty, and the fields defaults and possible values are populated via javascript.

There are two important javascript variables sent from the server, ``TaoMetadata`` and ``TaoJob``. ``TaoMetadata`` contains all the database options for creating a job, ``TaoJob`` contains parameter values to initialise the fields with. ``TaoJob`` will be empty if the user creates a new job, but will be populated if a user uploads a parameter file or selects a preset.

Catalogue.js

Each UI Mmodule has its own javascript file located deep in its static subfolder, for the SED module the file is located in ``ui/sed/taoui_sed/static/js/taoui_sed/sed.js``. These modules conform to a simple interface that allows ``catalogue.js`` to control the initialisation of modules::

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

Modules are also responsible for both client and server side validtion. On the client side, ``catalogue.js`` contains a number of validators in the form of knockout extensions, but you can add more as required. 

Below is an example of a field from the Light-Cone module being initialised with validators::

    param = job['light_cone-redshift_min'];
    vm.redshift_min = ko.observable(param ? param : null)
        .extend({required: function(){return vm.catalogue_geometry().id == 'light-cone'}})
        .extend({only_if: function(){return vm.catalogue_geometry().id == 'light-cone'}})
        .extend({validate: catalogue.validators.is_float})
        .extend({validate: catalogue.validators.geq(0)});


