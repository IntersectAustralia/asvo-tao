
var catalogue = catalogue || {};
<<<<<<< HEAD
catalogue.modules = catalogue.modules || {};

catalogue.modules.record_filter = function ($) {
=======
catalogue.module_defs = catalogue.module_defs || {};

catalogue.module_defs.record_filter = function ($) {
>>>>>>> work

    // KO ViewModel
    var vm = {}
    this.vm = vm;

    this.cleanup_fields = function ($form) {
    }

    this.validate = function ($form) {
    	return true;
    }

    this.pre_submit = function ($form) {

    }

    this.job_parameters = function() {
    	var params = {
    		'record_filter-filter': [vm.selection().value],
    		'record_filter-min': [vm.selection_min()],
    		'record_filter-max': [vm.selection_max()]
    	}
    	return params;
    }

    var to_option = function(obj) {
        if (obj.model === "tao.datasetproperty") {
            return {
    			value: 'D-'+obj.pk,
    			label: obj.fields.label + (catalogue.validators.defined(obj.fields.units) ?
                    ' ('+obj.fields.units+')' : '')
    		}
        } else if (obj.model === "tao.bandpassfilter") {
                return {
                    value: 'B-'+obj.pk,
                    label: obj.fields.label
                }
        } else {
            throw "cant_filter_on " + obj.model;
        }
    }

    var filter_choices = function () {
    	// Build up the list of fields that the user can filter records on:
    	// * Selected output properties with is_filter true
    	// * Selected bandpass filters
    	// * The dataset default filter
    	// Note that a filter selection is required, i.e.
    	// the No Filter options has been removed
    	var default_filter_pk;
    	var output_properties;
    	var bandpass_filters;
    	var current_selection = vm.selection();
        var result = [];
        var defined = catalogue.validators.defined;

        // If KO find the same object in the options, will keep it selected
        // so this helper function ensures that
        function add_to_result(obj) {
            if (obj === undefined) return;
            if (current_selection !== undefined && obj.value == current_selection.value) {
                result.push(current_selection)
            } else {
                result.push(obj);
            }
        }

    	// Get the default filter
<<<<<<< HEAD
    	default_filter_pk = catalogue.modules.light_cone.vm.dataset().fields.default_filter_field;
        if (defined(default_filter_pk)) {
            var def_dataset = catalogue.util.dataset_property(default_filter_pk);
            if (defined(def_dataset)) {
    	        add_to_result(to_option(catalogue.util.dataset_property(default_filter_pk)));
            }
        }
=======
        // Disabled for ticket ASVO-640
    	// default_filter_pk = catalogue.modules.light_cone.vm.dataset().fields.default_filter_field;
     //    if (defined(default_filter_pk)) {
     //        var def_dataset = catalogue.util.dataset_property(default_filter_pk);
     //        if (defined(def_dataset)) {
    	//         add_to_result(to_option(catalogue.util.dataset_property(default_filter_pk)));
     //        }
     //    }
>>>>>>> work

    	// Get the selected output properties with is_filter==true
    	output_properties = catalogue.modules.light_cone.vm.output_properties();
    	for (var i=0; i<output_properties.length; i++) {
    		var output_property = output_properties[i];
    		if (output_property.pk == default_filter_pk) {
    			continue; // It's already been added above
    		}
    		if (output_property.fields.is_filter) {
    			add_to_result(to_option(output_property));
    		}
    	}

<<<<<<< HEAD
        if (catalogue.modules.sed.vm.apply_sed()) {
=======

    	// Re-enabled by A Hassan V 1.01  Release
        if (catalogue.modules.sed.vm.apply_sed() && catalogue.modules.sed.vm.can_have_sed()) {
>>>>>>> work
            // Get the selected bandpass filters
            bandpass_filters = catalogue.modules.sed.vm.bandpass_filters();
            for (var i=0; i<bandpass_filters.length; i++) {
                add_to_result(to_option(bandpass_filters[i]));
            }
        }

    	return result;
    }
    
    var filter_choice = function(id) {
    	return $.grep(filter_choices(), function(elem, idx) {
    		return elem.value == id;
    	})[0];
    }

    var valid_min_max = function() {
    	// Ensure that max is greater than min
    	rs_max = vm.selection_max();
    	rs_min = vm.selection_min();
    	
        if (rs_max === undefined || rs_max === null || rs_max == '')
            return {'error': false};
        if (rs_min === undefined || rs_min === null || rs_min == '')
            return {'error': false};
        if (parseFloat(rs_max) > parseFloat(rs_min))
        	return {'error': false}
        else
        	return {'error': true, message: 'Selection max must be greater than Selection min'}
    }
    
    this.hr_summary = function() {
    	var res = '';
    	if (vm.selection() == undefined) {
    		return '';
    	}
    	var smin = vm.selection_min();
    	var smax = vm.selection_max();
    	var label = vm.selection().label;

    	if (smin) {
    		res = res + smin + ' ≤ ';
    	}
    	res = res + label; 
    	if (smax) {
    		res = res + ' ≤ ' + smax;
    	}
    	return res;
    }

    this.init_model = function (init_params) {
    	var current_dataset;
    	// job is either an object containing the job parameters or null
    	var job = init_params.job;
    	var param; // Temporary variable for observable initialisation
        var defined = catalogue.validators.defined;

<<<<<<< HEAD
    	vm.selection = ko.observable();
    	
    	vm.selections = ko.computed(filter_choices);
    	current_dataset = catalogue.modules.light_cone.vm.dataset();

        param = job['record_filter-filter'];
        if (param) {
            param = catalogue.util.get_observable_by_attribute('value', param, vm.selections);
            if(param) {
                vm.selection(param);
            }
        }

    	// Create the min and max observables
    	// Set up validation after creation as we have a validator that refers to both observables
        
        param = job['record_filter-min']
        vm.selection_min = ko.observable(param ? param : current_dataset.fields.default_filter_min)
        
        param = job['record_filter-max']
        vm.selection_max = ko.observable(param ? param : current_dataset.fields.default_filter_max)
=======
    	vm.selection = ko.observable().extend({required: true});
    	
    	vm.selections = ko.computed(filter_choices);
        // Disabled for ticket ASVO-640
    	// current_dataset = catalogue.modules.light_cone.vm.dataset();
        // vm.selection_min = ko.observable(current_dataset.fields.default_filter_min);
        // vm.selection_max = ko.observable(current_dataset.fields.default_filter_max);
        vm.selection_min = ko.observable();
        vm.selection_max = ko.observable();

        // Create the min and max observables
        // Set up validation after creation as we have a validator that refers to both observables
>>>>>>> work

        vm.selection_min
            .extend({required: function(){
                return !defined(vm.selection_max());
            }})
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: valid_min_max});

        vm.selection_max
            .extend({required: function(){
                return !defined(vm.selection_min());
            }})
<<<<<<< HEAD
    		.extend({validate: catalogue.validators.is_float})
    		.extend({validate: valid_min_max});
=======
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: valid_min_max});

        param = job['record_filter-filter'];
        if (param) {
            param = catalogue.util.get_observable_by_attribute('value', param, vm.selections);
            if(param) {
                vm.selection(param);
                if ('record_filter-min' in job) {
                    vm.selection_min(job['record_filter-min'])
                }
                if ('record_filter-max' in job) {
                    vm.selection_max(job['record_filter-max'])
                }
            }
        }
>>>>>>> work

    	vm.hr_summary = ko.computed(this.hr_summary);

    	return vm;
    }

}