
var catalogue = catalogue || {};
catalogue.module_defs = catalogue.module_defs || {};


catalogue.module_defs.light_cone = function ($) {


    function get_widget() {
        return catalogue.modules.light_cone.lc_output_props_widget;
    }

    // KO ViewModel
    var vm = {}
    this.the_vm = vm;

    var calculate_job_size = function() {
    	// Calculate the job size (percentage of max allowed size) based on the current cone parameters
    	var cjs;
    	// Retrieve constants
    	var job_size_p1 = parseFloat(vm.dataset().fields.job_size_p1);
    	var job_size_p2 = parseFloat(vm.dataset().fields.job_size_p2);
    	var job_size_p3 = parseFloat(vm.dataset().fields.job_size_p3);
    	var box_size = parseFloat(vm.dark_matter_simulation().fields.box_size);
    	var H0; // This should be a dataset parameter
    	var max_job_box_count = parseInt(vm.dataset().fields.max_job_box_count);

    	// Temporary hack for H0
    	// This should be retrieved as a dataset parameter
    	if (vm.dark_matter_simulation().fields.name == 'Bolshoi') {
    		H0 = 70.0
    	} else {
    		H0 = 73.0
    	}
    	// Get user input parameters
    	var ra_min = parseFloat(vm.ra_min());
    	var dec_min = parseFloat(vm.dec_min());
    	var ra_max = parseFloat(vm.ra_max());
    	var dec_max = parseFloat(vm.dec_max());
    	var z_min = parseFloat(vm.redshift_min());
    	var z_max = parseFloat(vm.redshift_max());

    	// Return something useful if not all parameters have been entered
    	if (isNaN(ra_max) || isNaN(dec_max) || isNaN(z_min) || isNaN(z_max)) {
    		return null;
    	}
    	cjs = job_size.job_size(box_size, ra_min, ra_max, dec_min, dec_max, z_min, z_max, H0,
    			max_job_box_count, job_size_p1, job_size_p2, job_size_p3);
    	return Math.round(cjs * 100);
    }

    this.cleanup_fields = function ($form) {
    }

    this.pre_submit = function ($form) {
    }

    this.job_parameters = function() {
    	var geometry = vm.catalogue_geometry().id;
    	var output_props = vm.output_properties();
    	var output_ids = [];
    	for (var i=0; i<output_props.length; i++) {
    		output_ids.push(output_props[i].pk);
    	}
    	var params = {
    		'light_cone-catalogue_geometry': [geometry],
    		'light_cone-dataset_id' : [vm.dataset().pk],
    		'light_cone-dark_matter_simulation': [vm.dark_matter_simulation().pk],
    		'light_cone-galaxy_model': [vm.galaxy_model().pk],
    		'light_cone-output_properties': output_ids
    	};
    	if (geometry == "box") {
    		jQuery.extend(params, {
    			'light_cone-snapshot': [vm.snapshot().pk],
    			'light_cone-box_size': [vm.box_size()],
                'light_cone-rng_seed': vm.rng_seed
    		});
    	} else { // light-cone
            if (vm.light_cone_type() == 'random') {
                jQuery.extend(params, {'light_cone-rng_seeds': vm.rng_seeds()});
            }
    		jQuery.extend(params, {
    			'light_cone-light_cone_type': [vm.light_cone_type()],
    			'light_cone-ra_min': [vm.ra_min()],
    			'light_cone-dec_min': [vm.dec_min()],
    			'light_cone-ra_max': [vm.ra_max()],
    			'light_cone-dec_max': [vm.dec_max()],
    			'light_cone-number_of_light_cones': [parseInt(vm.number_of_light_cones())],
    			'light_cone-redshift_min': [vm.redshift_min()],
    			'light_cone-redshift_max': [vm.redshift_max()],
    		});
    	}
    	return params;
    }

    var dataset_property_to_option = function(dsp) {
        return {
            'value': dsp.pk,
            'text' : dsp.fields.label,
            'group': dsp.fields.group,
            'units': dsp.fields.units,
            'order': dsp.fields.order
        }
    }

    var format_redshift = function(redshift_string) {
        var redshift = parseFloat(redshift_string);
        var whole_digit = parseInt(redshift).toString().length;
        return redshift.toFixed(Math.max(5 - whole_digit, 0));
    };

    this.format_redshift = format_redshift;

    var lookup_dataset = function(sid, gmid) {
    	var res = $.grep(TaoMetadata.DataSet, function(elem, idx) {
    		return elem.fields.simulation == sid && elem.fields.galaxy_model == gmid;
    	});
    	return res[0];
    };

    var lookup_geometry = function(gid) {
    	var res = $.grep(vm.catalogue_geometries(), function(elem, idx) {
    		return elem.id == gid;
    	});
    	return res[0];
    }

    var available_datasets = function() {
    	// Answer the set of available datasets
    	var res = $.grep(TaoMetadata.DataSet, function(elem, idx) {
    		return elem.fields.available;
    	});
    	return res;
    }

    var available_simulations = function() {
    	// Answer the set of simulations that are available
    	// Only those that are associated with active datasets are available
    	var sids = [];
    	var datasets = available_datasets();
    	for (var i=0; i<datasets.length; i++) {
    		sids.push(datasets[i].fields.simulation);
    	}
    	var res = $.grep(TaoMetadata.Simulation, function(elem, idx) {
    		return sids.indexOf(elem.pk) >= 0;
    	});
    	return res;
    }

    var available_galaxy_models = function(sid) {
    	// Answer the set of galaxy models that are available
    	// Only those that are associated with active datasets from current simulation id (sid)
    	// are available
    	var sids = [];
    	var datasets = available_datasets();
    	for (var i=0; i<datasets.length; i++) {
            if (datasets[i].fields.simulation == sid) {
    		    sids.push(datasets[i].fields.galaxy_model);
            }
    	}
    	var res = $.grep(TaoMetadata.GalaxyModel, function(elem, idx) {
    		return sids.indexOf(elem.pk) >= 0;
    	});
    	return res;
    }

    this.init_model = function(init_params) {
    	// job is either an object containing the job parameters or null
    	var job = init_params.job;
    	var param; // Temporary variable for observable initialisation
        var default_dataset_id;

        this.vm = vm;
        vm.catalogue_geometries = ko.observableArray([
            { id: 'light-cone', name: 'Light-Cone', bit_mask:1},
            { id: 'box', name: 'Box', bit_mask:2}
            ]);
        param = job['light_cone-catalogue_geometry']
        if (param)
        	param = lookup_geometry(param);
        vm.catalogue_geometry = ko.observable(param ? param : vm.catalogue_geometries()[1]);

        var default_dataset_param = catalogue.util.global_parameter('default_dataset');
        var defined = catalogue.validators.defined
        if (defined(default_dataset_param)) {
            default_dataset_id = default_dataset_param.fields.parameter_value;
        } else {
            default_dataset_id = TaoMetadata.DataSet[0]['pk'];
            console.log("No default_dataset value supplied in GlobalParameters. Using the first dataset stored in the Database as default.");
        }
        var default_dataset = catalogue.util.dataset(parseInt(default_dataset_id));
        if (!defined(default_dataset)) {
            default_dataset = TaoMetadata.DataSet[0];
            console.log("No dataset found for the default_dataset ID supplied. Using the first dataset stored in the Database as default.");
        }
        vm.dark_matter_simulations = ko.observableArray(available_simulations());
        param = job['light_cone-dark_matter_simulation'];
        if (param) {
        	param = catalogue.util.simulation(param);
        } else {
            param = catalogue.util.simulation(default_dataset.fields['simulation']);
        }
        vm.dark_matter_simulation = ko.observable(param ? param : vm.dark_matter_simulations()[0])
        	.extend({logger: 'simulation'});

        vm.galaxy_models = ko.computed(function(){
            return available_galaxy_models(vm.dark_matter_simulation().pk);
        });
        param = job['light_cone-galaxy_model'];
        if (param) {
        	param = catalogue.util.galaxy_model(param);
        } else {
            param = catalogue.util.galaxy_model(default_dataset.fields['galaxy_model']);
        }
        vm.galaxy_model = ko.observable(param ? param : vm.galaxy_models()[0]);

        vm.datasets = ko.observableArray(available_datasets());
        vm.dataset = ko.computed(function() {
        	// Answer the current dataset based on the current simulation and galaxy model
        	return lookup_dataset(vm.dark_matter_simulation().pk,
        						  vm.galaxy_model().pk);
        }).extend({logger: 'dataset'});

        vm.snapshots = ko.computed(function (){
            return catalogue.util.snapshots(vm.dataset().pk)
        });
        param = catalogue.util.snapshot(job['light_cone-snapshot']);
        vm.snapshot = ko.observable(param ? param : vm.snapshots()[0]);
        vm.simulation_redshift_max = ko.observable(vm.snapshots()[vm.snapshots().length-1].fields.redshift);
        vm.snapshots.subscribe(function(arr){
            vm.snapshot(arr[0]);
            vm.simulation_redshift_max(arr[arr.length-1].fields.redshift);
        });
        

        param = job['light_cone-light_cone_type'];
        vm.light_cone_type = ko.observable(param ? param : 'unique');

        param = job['light_cone-ra_min'];
        vm.ra_min = ko.observable(param ? param : null)
            .extend({required: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({only_if: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(0)})
            .extend({validate: catalogue.validators.leq(90)});

        param = job['light_cone-ra_max'];
        vm.ra_max = ko.observable(param ? param : null)
            .extend({required: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({only_if: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(0)})
            .extend({validate: catalogue.validators.leq(90)})
            .extend({validate: catalogue.validators.greater_than(vm.ra_min)});



        param = job['light_cone-dec_min'];
        vm.dec_min = ko.observable(param ? param : null)
            .extend({required: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({only_if: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(0)})
            .extend({validate: catalogue.validators.leq(90)});


        param = job['light_cone-dec_max'];
        vm.dec_max = ko.observable(param ? param : null)
            .extend({required: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({only_if: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(0)})
            .extend({validate: catalogue.validators.leq(90)})
            .extend({validate: catalogue.validators.greater_than(vm.dec_min)});

						  
		  	
        param = job['light_cone-redshift_min'];
        vm.redshift_min = ko.observable(param ? param : null)
            .extend({required: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({only_if: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(0)});

        param = job['light_cone-redshift_max'];
        vm.redshift_max = ko.observable(param ? param : null)
            .extend({required: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({only_if: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.greater_than(vm.redshift_min)})
            .extend({validate: catalogue.validators.greater_than(0)})
            .extend({validate: catalogue.validators.leq(vm.simulation_redshift_max)});

        vm.max_box_size = ko.computed(function() {
            return vm.dark_matter_simulation().fields.box_size
        });

        param = job['light_cone-box_size'];
        vm.box_size = ko.observable(param ? param : vm.max_box_size())
            .extend({required: function(){return vm.catalogue_geometry().id == 'box'}})
            .extend({only_if: function(){return vm.catalogue_geometry().id == 'box'}})
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(0)})
            .extend({validate: catalogue.validators.leq(vm.max_box_size)});

        // Note: these KO observables rely on observables defined above
        // so keep them here
        vm.maximum_number_of_light_cones = ko.computed(function() {
            if (vm.catalogue_geometry().id == 'box') return NaN;
            try {
            	__max = get_global_maximum_light_cones();
                var resp = vm.light_cone_type() == 'random' ? __max
                    : get_number_of_unique_light_cones();
                if (resp == null || resp === undefined || isNaN(resp)) {
                	return NaN;
                } else if (resp > __max) {
                	return __max;
                } else {
                	return resp;
                }
            } catch (e) {
                return NaN;
            }
        });

        param = job['light_cone-number_of_light_cones'];
        vm.number_of_light_cones = ko.observable(param ? param : 1)
            .extend({required: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({only_if: function(){return vm.catalogue_geometry().id == 'light-cone'}})
            .extend({validate: catalogue.validators.test(ko.computed(
                function(){
                    var max = vm.maximum_number_of_light_cones();
                    return max != null && !isNaN(max) && max >= 1;
                }
            ),
            "Cannot validate number of light cones.")})
            .extend({validate: catalogue.validators.is_int})
            .extend({validate: catalogue.validators.geq(1)})
            .extend({validate: catalogue.validators.leq(vm.maximum_number_of_light_cones)})
            .extend({logger: 'number_of_light_cones'});

        vm.light_cones_msg = ko.computed( function() {
            result = vm.number_of_light_cones() + ' ' + vm.light_cone_type() + ' light-cone';
            result += vm.number_of_light_cones() > 1 ? 's' : '';
            return result;
        });



        param = job['light_cone-output_properties'];
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
            return catalogue.util.output_choices(vm.dataset().pk, vm.catalogue_geometry().bit_mask);
        });
        vm.output_properties = ko.observableArray(param ? param : [])
            .extend({required: function(){return true;}});
        vm.output_properties_widget = TwoSidedSelectWidget({
            elem_id: lc_id('output_properties'),
            options: vm.output_properties_options,
            selectedOptions: vm.output_properties,
            maximum_selection:null,
            to_option: dataset_property_to_option
        });
        vm.dataset.subscribe(function(v) {
        	// Any change in the dataset clears the selected output properties
        	vm.output_properties([]);
        })

        vm.current_output_property = ko.observable(undefined);
        vm.output_properties_widget.clicked_option.subscribe(function(v) {
            var op = catalogue.util.dataset_property(v);
            vm.current_output_property(op);
        });

        // Computed Human-Readable Summary Fields
        vm.estimated_cone_size = ko.computed(function(){
            try {
                var resp = calculate_job_size();
                if (resp == null)
                    return NaN;
                return resp;
            } catch(e) {
                return NaN;
            }
        });

        vm.estimated_cone_size_msg = ko.computed(function () {
        	var ecs = vm.estimated_cone_size();
        	var msg = 'Estimated job size: ';
        	if (isNaN(ecs)) {
        		msg += "(waiting for valid cone parameters)";
                return msg;
        	}
            msg = msg + ecs + "%";
            if (ecs > 100) {
                var warning = catalogue.util.global_parameter_or_null('job_too_large_warning');
                if (warning == null) {
                    warning = '<i><em>NOTE:</em> This job may not complete within the allowed time.</i>';
                } else {
                    warning = warning.fields.parameter_value;
                }
                msg += ' ' + warning;
            }
            return msg;
        });

        vm.hr_ra_opening_angle = ko.computed(function(){
            var result = '< RA <';
            
            if (vm.ra_max() != undefined && /\S/.test(vm.ra_max())) {
                result +=  vm.ra_max()+'&deg;';
                if (vm.ra_min() != undefined && /\S/.test(vm.ra_min())) 
					 {
                    result = vm.ra_min()+'&deg;'+ result; 
                } 
            }
            return result+= '<br>';
        });


        vm.hr_dec_opening_angle = ko.computed(function(){
            var result = '< Dec <';
            
            if (vm.dec_max() != undefined && /\S/.test(vm.dec_max())) {
                result +=  vm.dec_max()+'&deg;';
                if (vm.dec_min() != undefined && /\S/.test(vm.dec_min())) 
					 {
                    result = vm.dec_min()+'&deg;'+ result; 
                } 
            }
            
            
            return result+= '<br>';
        });
        

			        
        


        vm.hr_redshift = ko.computed(function() {
            var result = '';
            if (vm.catalogue_geometry().id == 'light-cone') {
                var rs_min = vm.redshift_min() != undefined && /\S/.test(vm.redshift_min());
                var rs_max = vm.redshift_max() != undefined && /\S/.test(vm.redshift_max());
                if (rs_min && !rs_max) {
                    result = 'Redshift: ' + vm.redshift_min() + ' &le; z' ;
                } else if (!rs_min && rs_max) {
                    result = 'Redshift: z &le; ' + vm.redshift_max();
                } else if (rs_min && rs_max) {
                    result = 'Redshift: ' + vm.redshift_min() + ' &le; z &le; ' + vm.redshift_max();
                }
            } else {
                var snapshot = vm.snapshot();
                if (snapshot !== undefined)
                    result = format_redshift(vm.snapshot().fields.redshift);
            }
            return result;
        });

        var int_width = Math.pow(2, 32);

        var random_seed = function() {
            // signed 32 bit integer
            return Math.floor((Math.random() * int_width) -
			(int_width / 2));
        }

        vm.rng_seed = TaoJob['light_cone-rng_seed'] ? TaoJob['light_cone-rng_seed'] : random_seed();
        vm.rng_seeds = ko.computed(function() {
            result = [];
            var i = 0;
            for (i; i < vm.number_of_light_cones(); i++) {
                var key = 'rng-seed-' + i
                if(TaoJob['light_cone-rng_seeds'] && TaoJob['light_cone-rng_seeds'][key]) {
                    result.push(parseInt(TaoJob['light_cone-rng_seeds'][key]));
                } else {
                    result.push(random_seed());
                }
            }
            return result;
        });

        vm.number_of_light_cones_msg = ko.computed(function() {
            var result = '';
            var lc = vm.maximum_number_of_light_cones();
            if (isNaN(lc)) {
                result = '(waiting for valid cone parameters)';
            } else if (vm.light_cone_type() == 'unique' && (vm.ra_min() >0 || vm.dec_min()>0)) {				 
                result = 'You cannot select Unique Light-cone with RA min >0 or DEC Min >0 ';      
            } else if (lc < 1) {
                result = 'The current light-cone dimension exceeds the available simulation space.<br/>Please reduce the light-cone dimensions or change to random light-cones.';
				                 
            } else {
                result = 'maximum is ' + lc;
            }
            return result;
        });

        return vm;

    }

}
