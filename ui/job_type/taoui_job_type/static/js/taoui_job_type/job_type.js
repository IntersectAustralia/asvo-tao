// create the namespace if it doesn't exist
var catalogue = catalogue || {}; 
catalogue.module_defs = catalogue.module_defs || {};
 
// jQuery is passed as a parameter to ensure jQuery plugins work correctly
catalogue.module_defs.job_type = function ($) {
    // KO ViewModel
    var vm = {}

    this.cleanup_fields = function ($form) {
        // clear values from exluded fields
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
            $('#survey_presets').toggle();
            $('#survey_presets_info_box').toggle();
        });

    }

    this.init_model = function (init_params) {
        // setup state
        vm.survey_presets = ko.observableArray(TaoMetadata['SurveyPreset']);
        vm.selected_survey_preset = ko.observable(vm.survey_presets()[0]);
        this.vm = vm;
        // initialise event handlers
        init_event_handlers();
        return vm;
    }
}
