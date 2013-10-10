Introduction

This section describes the framework used to manage the JavaScript which accompanies a UI module, and how to implement the interface when creating additional modules. In addition to the commonly used jQuery library, the interface relies heavily on the Knockout.js library and it is recommended that you familiarise yourself with its concepts before delving into this section.

UI Module Lifecycle

The html form elements sent from the server start of empty, and it's the javascript that sets the possible values for the fields, sets the default values, and performs client side validation.

The values that a field 