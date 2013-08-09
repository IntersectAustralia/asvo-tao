// create the namespace if it doesn't exist
var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};

// jQuery is passed as a parameter to ensure jQuery plugins work correctly
catalogue.modules.output_format = function ($) {

    // KO ViewModel
	var vm = {};
	this.vm = vm;

	this.configured_output_formats = function() {
		// Answer the list of output_formats configured in Global Parameters
		// Raise an exception if the parameter is missing
		var output_formats = [];
		var params_string = catalogue.util.global_parameter_or_null('output_formats');
		
		if (params_string == null) {
			var msg = "Unable to retrieve output properties"; 
			alert(msg);
			console.log(msg);
			return null;
		}
		params_string = params_string.fields.parameter_value;
		source_params = eval(params_string);
		for (var i=0; i<source_params.length; i++) {
			output_formats.push({
				pk: i,
				model: 'output_formats',
				fields: source_params[i]
			});
		}
		
		return output_formats;
	}
	
    this.cleanup_fields = function ($form) {
        // always send everything from the Output Format tab through to the server
    	// i.e. nothing to do
    	return;
    }

    this.validate = function ($form) {
    	// The module is valid as long as a supported output format is selected.
        return this.vm.output_formats().indexOf(vm.output_format()) >= 0;
    }

    this.pre_submit = function ($form) {
    	// Nothing to do?
    	return;
    }
    
    this.job_parameters = function() {
    	var params = {
    			'output_format-supported_formats': [this.vm.output_format().fields.value]
    	}
    	return params;
    }


    this.init_model = function () {
    	
    	this.vm.output_formats = ko.observableArray(this.configured_output_formats());
    	this.vm.output_format = ko.observable(this.vm.output_formats()[0]);

        return this.vm;
    }
}
