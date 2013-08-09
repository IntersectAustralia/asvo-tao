// create the namespace if it doesn't exist
var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};

// jQuery is passed as a parameter to ensure jQuery plugins work correctly
catalogue.modules.output_format = function ($) {

    // KO ViewModel
	var vm = {}
    this.the_vm = vm;

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

    this.init_model = function () {
    	
    	vm.output_formats = ko.observableArray(this.configured_output_formats());
    	vm.output_format = ko.observable(vm.output_formats()[0]);

        return vm;
    }
}
