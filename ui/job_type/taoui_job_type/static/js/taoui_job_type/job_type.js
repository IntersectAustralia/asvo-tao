// create the namespace if it doesn't exist
var catalogue = catalogue || {}; 
catalogue.modules = catalogue.modules || {};
 
// jQuery is passed as a parameter to ensure jQuery plugins work correctly
catalogue.modules.job_type = function ($) {
 
    var vm = {}
 
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
        // makes it possible to load a file after clicking 'back'
        $(document).ready(function() {
            $('#id_job_type-params_file').val("");
        });

        $('#id_job_type-params_file').change(function() {
            $('#file_upload').submit();
        });

        $('#presets_button').click(function() {
            $('#survey_presets').toggle('slide', {direction: 'up'});
        });
    }

    this.init_model = function (init_params) {
        // setup state
        vm.survey_presets = ko.observableArray(TaoMetadata['SurveyPreset']);
        // initialise event handlers
        init_event_handlers();

        return vm;
    }
}
