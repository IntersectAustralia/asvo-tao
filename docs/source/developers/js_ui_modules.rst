Introduction

This document describes the framework used to manage the JavaScript which accompanies a UI module, and how to implement the interface when creating additional modules.

The architecture came about from a major refactoring which attempted to separate a single single humongous JavaScript file into component modules. The major issues that arose related to event timing and closely coupled components. This framework attempts to address the first issue by managing the lifecycle of the modules, and the second issue is a work-in-progress.

Framework

Organisation

The framework is organised into the catalogue namespace.

catalogue.util is used for functions shared across the modules
catalogue.module is the container for the modules themselves, with each module defining its own subpath within the namespace, e.g. catalogue.modules.sed
Lifecycle
catalogue.js manages the lifecycle of the modules, which is broken down into the five phases. The first two phases occur when the DOM has been created, and the last three occur when the form's submission button has been clicked.
When the jQuery(document).ready() event is triggered:

1. Creation: all modules are created.

2. Initialisation: after all modules have been created, the module's init() function is called. This method should set up any initial state, and attach event handlers (conventionally by implementing an init_event_handlers() function).

When the form submit() event is triggered:

3. Field-cleanup: each module's cleanup_fields() function is called. Where there are mutually exclusive fields available, this method should be used to remove any data that has been placed in an excluded field prior to validation.

4. Validation: each module's validate() method is called, which should return a boolean value indicated whether all the module's fields are valid or not, and attach any error messages where appropriate.

5. Presubmission: each module's pre-submit() method is called, which should be used to preform any final work before submission.
Of these last three phases, only validate() is required to return a value, the other method bodies can be blank.

Minimal Interface

Below is a template that can be used as a the starting point for a new module.::

    // create the namespace if it doesn't exist
    var catalogue = catalogue || {}; 
    catalogue.modules = catalogue.modules || {};

    // jQuery is passed as a parameter to ensure jQuery plugins work correctly
    catalogue.modules.some_module = function ($) {

        this.cleanup_fields = function ($form) {
            // clear values from exluded fields
        }

        this.validate = function ($form) {
            // perform validations and
            // attach error messages
            return true;
        }

        this.pre_submit = function ($form) {
            // final activities before submission
        }

        function init_event_handlers() {
            // attach event handlers
        }
        this.init = function () {
            // setup state
            // initialise event handlers
            init_event_handlers();
        }
    }

