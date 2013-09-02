
var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};

catalogue.modules.sql_job = function ($) {

    function get_widget() {
    	return catalogue.modules.sql_job.sql_output_props_widget;
    }

    // KO ViewModel
    var vm = {}
    this.the_vm = vm;

    this.cleanup_fields = function ($form) {
    }

    this.validate = function ($form) {
    	var is_valid = true;
    	is_valid &= catalogue.util.validate_vm(vm);
    	return is_valid;
    }

    this.pre_submit = function ($form) {
    }

    this.sql_job_parameters = function() {
    	var output_props = vm.output_properties();
    	var output_ids = [];
    	for (var i=0; i<output_props.length; i++) {
    		output_ids.push(output_props[i].pk);
    	}
    	var params = {
    		'sql_job-dataset_id' : [vm.dataset().pk],
    		'sql_job-dark_matter_simulation': [vm.dark_matter_simulation().pk],
    		'sql_job-galaxy_model': [vm.galaxy_model().pk],
    		'sql_job-output_properties': output_ids
    	};
    	return params;
    }
    
    var dataset_property_to_option = function(dsp) {
        return {
            'value': dsp.pk,
            'text' : dsp.fields.label,
            'units': dsp.fields.units
        }
    }

    var lookup_dataset = function(sid, gmid) {
    	res = $.grep(TaoMetadata.DataSet, function(elem, idx) {
    		return elem.fields.simulation == sid && elem.fields.galaxy_model == gmid;
    	});
    	return res[0];
    };
    
    var lookup_geometry = function(gid) {
    	res = $.grep(vm.catalogue_geometries(), function(elem, idx) {
    		return elem.id == gid;
    	});
    	return res[0];
    }
    
    var available_datasets = function() {
    	// Answer the set of available datasets
    	res = $.grep(TaoMetadata.DataSet, function(elem, idx) {
    		return elem.fields.available;
    	});
    	return res;
    }

    var available_simulations = function() {
    	// Answer the set of simulations that are available
    	// Only those that are associated with active datasets are available
    	var sids = [];
    	datasets = available_datasets();
    	for (var i=0; i<datasets.length; i++) {
    		sids.push(datasets[i].fields.simulation);
    	}
    	res = $.grep(TaoMetadata.Simulation, function(elem, idx) {
    		return sids.indexOf(elem.pk) >= 0;
    	});
    	return res;
    }
    
    var available_galaxy_models = function() {
    	// Answer the set of galaxy models that are available
    	// Only those that are associated with active datasets are available
    	var sids = [];
    	datasets = available_datasets();
    	for (var i=0; i<datasets.length; i++) {
    		sids.push(datasets[i].fields.galaxy_model);
    	}
    	res = $.grep(TaoMetadata.GalaxyModel, function(elem, idx) {
    		return sids.indexOf(elem.pk) >= 0;
    	});
    	return res;
    }

    this.init_model = function(init_params) {
    	// job is either an object containing the job parameters or null
    	var job = init_params.job;
    	var param; // Temporary variable for observable initialisation
    	var bit_mask = 2; // Mask for the SQL job output properties corresponds to the Box geometry
    	                                          
        vm.dark_matter_simulations = ko.observableArray(available_simulations());
        param = job['sql_job-dark_matter_simulation'];
        if (param) {
        	param = catalogue.util.simulation(param);
        }
        vm.dark_matter_simulation = ko.observable(param ? param : vm.dark_matter_simulations()[0])
        	.extend({logger: 'simulation'});
        
        vm.galaxy_models = ko.observableArray(available_galaxy_models());
        param = job['sql_job-galaxy_model'];
        if (param) {
        	param = catalogue.util.galaxy_model(param);
        }
        vm.galaxy_model = ko.observable(param ? param : vm.galaxy_models()[0]);

        vm.datasets = ko.observableArray(available_datasets());
        vm.dataset = ko.computed(function() {
        	// Answer the current dataset based on the current simulation and galaxy model
        	return lookup_dataset(vm.dark_matter_simulation().pk, vm.galaxy_model().pk);
        }).extend({logger: 'dataset'});

        param = job['sql_job-output_properties'];
        if (param) {
        	// If output properties have been provided, assume that we are only displaying
        	// the job, so we don't need to set up the TwoSidedSelectWidget
        	var props = [];
        	for (var i=0; i<param.length; i++) {
        		props.push(catalogue.util.dataset_property(param[i]));
        	}
        	param = props;
        }
        
        vm.output_properties_options = ko.computed(function(){
            return catalogue.util.output_choices(vm.dataset().pk, bit_mask);
        });
        
        vm.output_properties = ko.observableArray(param ? param : [])
            .extend({required: function(){return true;}});
        vm.output_properties_widget = TwoSidedSelectWidget({
            elem_id: '#id_sql_job-output_properties',
            options: vm.output_properties_options,
            selectedOptions: vm.output_properties,
            to_option: dataset_property_to_option
        });

        vm.current_output_property = ko.observable(undefined);
    	
        // if param is null assume that we are in the Catalogue wizard
    	// so set up the dependencies to update the display
        // otherwise leave it unlinked
        if (!param) {
	        vm.output_properties_widget.clicked_option.subscribe(function(v) {
	            var op = catalogue.util.dataset_property(v);
	            vm.current_output_property(op);
	        });
        }
        
        param = job['sql_job-query'];
        vm.query = ko.observable(param ? param : '');
        
        return vm;

    }

}
    