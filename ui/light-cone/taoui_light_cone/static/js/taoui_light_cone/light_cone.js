
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
    }


    this.pre_submit = function ($form) {
    }

    this.job_parameters = function() {
    	var geometry = vm.catalogue_geometry().id;
    	var output_props = catalogue.modules.light_cone.the_vm.output_properties.to_side.options_raw();
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
    		jQuery.extend(params, {
    			'light_cone-light_cone_type': [vm.light_cone_type()],
    			'light_cone-ra_opening_angle': [vm.ra_opening_angle()],
    			'light_cone-dec_opening_angle': [vm.dec_opening_angle()],
    			'light_cone-number_of_light_cones': [vm.number_of_light_cones()],
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
            'units': dsp.fields.units
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
    
    this.init_model = function() {
        this.vm = vm;
        vm.catalogue_geometries = ko.observableArray([
            { id: 'light-cone', name: 'Light Cone'},
            { id: 'box', name: 'Box'}
            ]);
        vm.catalogue_geometry = ko.observable(vm.catalogue_geometries()[1]);

        vm.dark_matter_simulations = ko.observableArray(TaoMetadata.Simulation);
        vm.dark_matter_simulation = ko.observable(vm.dark_matter_simulations()[1]).extend({logger: 'simulation'});
        
        vm.galaxy_models = ko.observableArray(TaoMetadata.GalaxyModel);
        vm.galaxy_model = ko.observable(vm.galaxy_models()[0]);

        vm.datasets = ko.observableArray(TaoMetadata.DataSet);
        vm.dataset = ko.computed(function() {
        	// Answer the current dataset based on the current simulation and galaxy model
        	return lookup_dataset(vm.dark_matter_simulation().pk,
        						  vm.galaxy_model().pk);
        }).extend({logger: 'dataset'});

        vm.light_cone_type = ko.observable('unique');
        vm.number_of_light_cones = ko.observable(1)
            .extend({validate: catalogue.validators.is_int})
            .extend({validate: catalogue.validators.geq(1)});
        vm.dataset.subscribe(function(dataset) {
            var objs = catalogue.util.output_choices(dataset.pk);
            vm.output_properties.new_options(objs);
        });

        vm.ra_opening_angle = ko.observable()
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(0)})
            .extend({validate: catalogue.validators.leq(90)});

        vm.dec_opening_angle = ko.observable()
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(0)})
            .extend({validate: catalogue.validators.leq(90)});

        vm.redshift_min = ko.observable()
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(0)});

        vm.redshift_max = ko.observable()
            .extend({validate: catalogue.validators.is_float})
            .extend({validate: catalogue.validators.geq(vm.redshift_min)});

        vm.max_box_size = ko.computed(function() {
            return vm.dark_matter_simulation().fields.box_size
        });

        vm.box_size = ko.observable(vm.max_box_size())
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
        vm.snapshot = ko.observable(vm.snapshots()[0]);

        // Twosided widget
        vm.output_properties = TwoSidedSelectWidget(
                lc_id('output_properties'),
                {not_selected:catalogue.util.output_choices(vm.dataset().pk),selected:[]},
                dataset_property_to_option);
        vm.current_output_property = ko.observable(undefined);
        vm.output_properties.clicked_option.subscribe(function(v) {
            var op = catalogue.util.dataset_property(v);
            vm.current_output_property(op);
        });


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
