
var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};


catalogue.modules.light_cone = function ($) {


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
    	var ra_max = parseFloat(vm.ra_opening_angle());
    	var dec_max = parseFloat(vm.dec_opening_angle());
    	var z_min = parseFloat(vm.redshift_min());
    	var z_max = parseFloat(vm.redshift_max());

    	// Return something useful if not all parameters have been entered
    	if (isNaN(ra_max) || isNaN(dec_max) || isNaN(z_min) || isNaN(z_max)) {
    		return null;
    	}
    	cjs = job_size.job_size(box_size, 0, ra_max, 0, dec_max, z_min, z_max, H0,
    			max_job_box_count, job_size_p1, job_size_p2, job_size_p3);
    	return Math.round(cjs * 100);
    }

    this.cleanup_fields = function ($form) {
    }


    this.validate = function ($form) {
    	var is_valid = true;
    	// var is_ok = catalogue.validators.is_ok;
        // if (vm.catalogue_geometry() == 'box') {
        //     if (!is_ok(vm.box_size)) return false;
        // } else {
        //     if (!is_ok(vm.box_size)) return false;
        //    /// TODO !!!
        // }
    	is_valid &= catalogue.util.validate_vm(vm);
    	is_valid &= vm.output_properties.to_side.options_raw().length > 0;
    	return is_valid;
    }


    this.pre_submit = function ($form) {
    }

    this.job_parameters = function() {
    	var geometry = vm.catalogue_geometry().id;
    	var output_props = vm.output_properties.to_side.options_raw();
    	var output_ids = [];
    	for (var i=0; i<output_props.length; i++) {
    		output_ids.push(output_props[i].value);
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
    			'light_cone-box_size': [vm.box_size()]
    		});
    	} else { // light-cone
    		var noc = parseInt(vm.number_of_light_cones());
    		// Work-around: Hiding the spinner seems to set the count to 0
    		if (noc == 0) {
    			noc = 1;
    		}
    		jQuery.extend(params, {
    			'light_cone-light_cone_type': [vm.light_cone_type()],
    			'light_cone-ra_opening_angle': [vm.ra_opening_angle()],
    			'light_cone-dec_opening_angle': [vm.dec_opening_angle()],
    			'light_cone-number_of_light_cones': [noc],
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

    var snapshot_id_to_redshift = function(snapshot_id) {
        // console.log(snapshot_id);
        res = $.grep(TaoMetadata.Snapshot, function(elem, idx) { 
            return elem.pk == snapshot_id
        })[0].fields.redshift;
        return format_redshift(res);
    };

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

        this.vm = vm;
        vm.catalogue_geometries = ko.observableArray([
            { id: 'light-cone', name: 'Light-Cone', bit_mask:1},
            { id: 'box', name: 'Box', bit_mask:2}
            ]);
        param = job['light_cone-catalogue_geometry']
        if (param)
        	param = lookup_geometry(param);
        vm.catalogue_geometry = ko.observable(param ? param : vm.catalogue_geometries()[1]);

        vm.dark_matter_simulations = ko.observableArray(available_simulations());
        param = job['light_cone-dark_matter_simulation'];
        if (param) {
        	param = catalogue.util.simulation(param);
        }
        vm.dark_matter_simulation = ko.observable(param ? param : vm.dark_matter_simulations()[0])
        	.extend({logger: 'simulation'});
        
        vm.galaxy_models = ko.observableArray(available_galaxy_models());
        param = job['light_cone-galaxy_model'];
        if (param) {
        	param = catalogue.util.galaxy_model(param);
        }
        vm.galaxy_model = ko.observable(param ? param : vm.galaxy_models()[0]);

        vm.datasets = ko.observableArray(available_datasets());
        vm.dataset = ko.computed(function() {
        	// Answer the current dataset based on the current simulation and galaxy model
        	return lookup_dataset(vm.dark_matter_simulation().pk,
        						  vm.galaxy_model().pk);
        }).extend({logger: 'dataset'});

        param = job['light_cone-light_cone_type'];
        vm.light_cone_type = ko.observable(param ? param : 'unique');
        param = job['light_cone-number_of_light_cones'];
        vm.number_of_light_cones = ko.observable(param ? param : 1)
            .extend({validate: catalogue.validators.is_int});
        // Disable geq 1 check until we can figure out why it is being 
        // set to 0.  job_params ensures that it is at least 1 before
        // submission.
        //    .extend({validate: catalogue.validators.geq(1)});
        // Debugging

        vm.number_of_light_cones.subscribe(function(n) {
        	if (n==0) { console.log('WARN: Number of light-cones = 0'); }
        });
        vm.available_output_properties = ko.computed(function(){
            return catalogue.util.output_choices(vm.dataset().pk, vm.catalogue_geometry().bit_mask);
        });
        vm.available_output_properties.subscribe(function(objs) {
            vm.output_properties.new_options(objs);
        });
        vm.dataset.subscribe(function(dataset) {
            var objs = catalogue.util.output_choices(dataset.pk);
            vm.output_properties.new_options(objs);
        });

        param = job['light_cone-ra_opening_angle'];
        vm.ra_opening_angle = ko.observable(param ? param : null)
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(0)})
            .extend({validate: catalogue.validators.leq(90)});

        param = job['light_cone-dec_opening_angle'];
        vm.dec_opening_angle = ko.observable(param ? param : null)
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(0)})
            .extend({validate: catalogue.validators.leq(90)});

        param = job['light_cone-redshift_min'];
        vm.redshift_min = ko.observable(param ? param : null)
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(0)});

        param = job['light_cone-redshift_max'];
        vm.redshift_max = ko.observable(param ? param : null)
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(vm.redshift_min)});

        vm.max_box_size = ko.computed(function() {
            return vm.dark_matter_simulation().fields.box_size
        });

        param = job['light_cone-box_size'];
        vm.box_size = ko.observable(param ? param : vm.max_box_size())
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(0)})
            // .extend({validate: catalogue.validators.leq(vm.max_box_size)});
            .extend({validate: catalogue.validators.leq(vm.max_box_size)});

        vm.maximum_number_of_light_cones = ko.computed(function() {
            if (vm.light_cone_type() == 'random') {
                return get_global_maximum_light_cones();
            }
            return get_number_of_unique_light_cones();
        });

        vm.snapshots = ko.computed(function (){
            return catalogue.util.snapshots(vm.dataset().pk)
        });
        param = catalogue.util.snapshot(job['light_cone-snapshot']);
        vm.snapshot = ko.observable(param ? param : vm.snapshots()[0]);

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
        vm.output_properties = TwoSidedSelectWidget(
        		lc_id('output_properties'),
                {not_selected: catalogue.util.output_choices(vm.dataset().pk, vm.catalogue_geometry().bit_mask),
                 selected: param ? param : []},
                dataset_property_to_option);
        vm.current_output_property = ko.observable(undefined);
    	// if param is null assume that we are in the Catalogue wizard
    	// so set up the dependencies to update the display
        // otherwise leave it unlinked
        if (!param) {
	        vm.output_properties.clicked_option.subscribe(function(v) {
	            var op = catalogue.util.dataset_property(v);
	            vm.current_output_property(op);
	        });
        }

        // Computed Human-Readable Summary Fields
        vm.estimated_cone_size = ko.computed(calculate_job_size);


        var job_too_large = function() {
            return vm.estimated_cone_size() > 100;
        }


        vm.estimated_cone_size_css = ko.computed(function() {
            return job_too_large() ? 'job_too_large_error' : '';
        });


        vm.estimated_cone_size_msg = ko.computed(function () {
        	var ecs = vm.estimated_cone_size();
        	var msg = 'Estimated job size: ';
        	if (ecs == null) {
        		msg += "(waiting for valid cone parameters)";
        	} else {
	            msg = msg + ecs + "%";
	            if (job_too_large()) {
	                msg += '. Note this exceeds the maximum allowed size, please reduce the light-cone size (RA, Dec, Redshift range).';
	            }
        	}
            return msg;
        });

        vm.hr_ra_opening_angle = ko.computed(function(){
            var result = '';
            if (vm.ra_opening_angle() != undefined && /\S/.test(vm.ra_opening_angle())) {
                result += 'RA: ' + vm.ra_opening_angle() + '&deg;'
                if (vm.dec_opening_angle() != undefined && /\S/.test(vm.dec_opening_angle())) {
                    result += ', '
                } else {
                    result += '<br>'
                }
            }
            return result;
        });


        vm.hr_dec_opening_angle = ko.computed(function() {
            var result = '';
            if (vm.dec_opening_angle() != undefined && /\S/.test(vm.dec_opening_angle())) {
                result += 'Dec: ' + vm.dec_opening_angle() + '&deg;<br>'
            }
            return result;
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
                result = format_redshift(vm.snapshot().fields.redshift);
            }
            return result;
        });

        return vm;

    }

}
