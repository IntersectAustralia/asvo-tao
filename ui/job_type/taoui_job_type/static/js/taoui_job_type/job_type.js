// create the namespace if it doesn't exist
var catalogue = catalogue || {}; 
catalogue.modules = catalogue.modules || {};
 
// jQuery is passed as a parameter to ensure jQuery plugins work correctly
catalogue.modules.job_type = function ($) {
 
 
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
 
    this.job_parameters = function() {
    	var params = {
    	}
    	return params;
    }

    function init_event_handlers() {
        // attach event handlers
        $('#id_job_type-params_file').change(function() {
            // console.log('submit');
            $('#file_upload').submit();
        });

        $('#presets_button').click(function() {
            $('#survey_presets').toggle('slide', {direction: 'up'});
        });
    }

    this.init_model = function (init_params) {
        // setup state
        // initialise event handlers
        init_event_handlers();

        return {};
    }
}
