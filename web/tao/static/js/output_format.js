// create the namespace if it doesn't exist
var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};

// jQuery is passed as a parameter to ensure jQuery plugins work correctly
catalogue.modules.output_format = function ($) {

    this.init_model = function () {
        return {};
    }
}
