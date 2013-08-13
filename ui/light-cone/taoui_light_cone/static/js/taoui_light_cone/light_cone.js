
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


    var display_maximum_number_light_cones = function ($field, msg) {
        var $enclosing = $field.closest('label.control-label');
        $enclosing.find('span.lc_number-inline').remove();
        if (msg == null) return;
        $field.after('<span class="lc_number-inline"></span>');
        $enclosing.find('span.lc_number-inline').text(msg);
        show_tab($enclosing, 0);
    }


    // var update_galaxy_model_options = function (simulation_id) {
    //     var $galaxy_model = $(lc_id('galaxy_model'));
    //     if (simulation_id === 0) {
    //         $galaxy_model.empty();
    //         $galaxy_model.change();
    //         return;
    //     }

    //     var upd = function (data) {
    //             var initial_data_set_id = $galaxy_model.val();
    //             $galaxy_model.empty();
    //             for (i = 0; i < data.length; i++) {
    //                 item = data[i];
    //                 $option = $('<option/>');
    //                 $option.attr('value', item.id);
    //                 $option.attr('data-galaxy_model_id', item.galaxy_model_id);
    //                 $option.attr('data-job_size_p1', item.job_size_p1);
    //                 $option.attr('data-job_size_p2', item.job_size_p2);
    //                 $option.attr('data-job_size_p3', item.job_size_p3);
    //                 $option.attr('data-max_job_box_count', item.max_job_box_count);
    //                 if (item.id == initial_data_set_id) {
    //                     $option.attr('selected', 'selected');
    //                 }
    //                 $option.html(item.name);
    //                 $galaxy_model.append($option);
    //             }
    //             $galaxy_model.change();
    //         };

    //     upd(catalogue.util.galaxy_models(simulation_id));

    // };


    // var show_simulation_info = function (simulation_id) {

    //     data = catalogue.util.simulation(simulation_id);
    //     $('div.simulation-info .name').html(data.fields.name);
    //     $('div.simulation-info .details').html(data.fields.details);
    //     $('div.simulation-info').show();
    //     catalogue.util.fill_in_summary('light_cone', 'simulation', data.fields.name);
    //     catalogue.util.fill_in_summary('light_cone', 'simulation_description', '<br><b>' + data.fields.name + ':</b><br>' + data.fields.details);
    //     $(lc_id('number_of_light_cones')).data("simulation-box-size", data.fields.box_size);

    // };


    // var spinner_check_value = function (new_value) {
    //     var ra = vm.ra_opening_angle();
    //     var dec = vm.dec_opening_angle();
    //     var redshift_min = $(lc_id('redshift_min')).val();
    //     var redshift_max = $(lc_id('redshift_max')).val();
    //     var $spinner = $(lc_id('number_of_light_cones')).closest('span');
    //     var maximum = $(lc_id('number_of_light_cones')).data('spin-max');
    //     if (new_value <= 1) {
    //         if (new_value <= 0) {
    //             catalogue.util.show_error($spinner, "Please provide a positive number of light-cones");
    //             catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', 'Negative number of light-cones is invalid');
    //             return false;
    //         }
    //     }

    //     if (maximum > 0) {
    //         $(lc_id('number_of_light_cones')).spinner("option", "max", maximum);
    //         if (new_value >= maximum) {
    //             if (new_value > maximum) {
    //                 catalogue.util.show_error($spinner, "The maximum is " + maximum);
    //                 catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', 'Number of light cones selected exceeds the maximum');
    //                 return false;
    //             }
    //         }

    //     } else if (ra != "" && dec != "" && redshift_min != "" && redshift_max != "") {
    //         catalogue.util.show_error($spinner, "Selection parameters can't be used to generate unique light-cones");
    //         catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', 'An invalid number of light cones is selected');
    //         return false;
    //     }

    //     catalogue.util.show_error($spinner, null);
    //     catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', new_value + " " + $("input[name='light_cone-light_cone_type']:checked").val() + " light cones");
    //     return true;
    // }


    var spinner_check_value = function (new_value) {
        var ra = vm.ra_opening_angle();
        var dec = vm.dec_opening_angle();
        // var redshift_min = $(lc_id('redshift_min')).val();
        // var redshift_max = $(lc_id('redshift_max')).val();
        var redshift_min = vm.redshift_min();
        var redshift_max = vm.redshift_max();

        var $spinner = $(lc_id('number_of_light_cones')).closest('span');
        var maximum = $(lc_id('number_of_light_cones')).data('spin-max');
        if (new_value <= 1) {
            if (new_value <= 0) {
                catalogue.util.show_error($spinner, "Please provide a positive number of light-cones");
                catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', 'Negative number of light-cones is invalid');
                return false;
            }
        }

        if (maximum > 0) {
            $(lc_id('number_of_light_cones')).spinner("option", "max", maximum);
            if (new_value >= maximum) {
                if (new_value > maximum) {
                    catalogue.util.show_error($spinner, "The maximum is " + maximum);
                    catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', 'Number of light cones selected exceeds the maximum');
                    return false;
                }
            }

        } else if (ra != "" && dec != "" && redshift_min != "" && redshift_max != "") {
            catalogue.util.show_error($spinner, "Selection parameters can't be used to generate unique light-cones");
            catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', 'An invalid number of light cones is selected');
            return false;
        }

        catalogue.util.show_error($spinner, null);
        catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', new_value + " " + $("input[name='light_cone-light_cone_type']:checked").val() + " light cones");
        return true;
    }

    var calculate_max_number_of_cones = function () {
        function spinner_set_max(maximum) {
            $spinner_label = $('label[for=id_light_cone-number_of_light_cones]');
            if (isNaN(maximum) || maximum <= 0 || !isFinite(maximum)) {
                $(lc_id('number_of_light_cones')).spinner("disable");
                $(lc_id('number_of_light_cones')).data("spin-max", 0);
                $spinner_label.html("Select the number of light-cones:*");
                catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', 'Invalid light-cone parameters selected');
                return false;
            } else {
                $(lc_id('number_of_light_cones')).spinner("enable");
                $(lc_id('number_of_light_cones')).data("spin-max", maximum);
            }
            spinner_check_value(parseInt($(lc_id('number_of_light_cones')).val()));
            return true;
        }

        var selection = $("input[name='light_cone-light_cone_type']:checked").val();

        if ("unique" == selection) {
            // TODO: remove lines below once observers point-of-view for multiple unique light cones has been fixed in science modules
            $(lc_id('number_of_light_cones')).val('1');
            $(lc_id('number_of_light_cones')).closest('div.control-group').hide();
            //////
            var maximum = get_number_of_unique_light_cones();
            if (spinner_set_max(maximum)) {
                $spinner_label.html("Select the number of light-cones: (maximum for the selected parameters is " + maximum + ")*");
            }
        } else {
            // TODO: remove line below once observers point-of-view for multiple unique light cones has been fixed in science modules
            $(lc_id('number_of_light_cones')).closest('div.control-group').show();
            //////

            var data = catalogue.util.global_parameter('maximum-random-light-cones');
            var maximum = parseInt(data.fields.parameter_value);
            if (spinner_set_max(maximum)) {
                $spinner_label.html("Select the number of light-cones: (maximum " + maximum + " random light-cones)*");
            }

        }
    }


    var validate_number_of_light_cones = function () {
        var geometry = vm.catalogue_geometry(); // $(lc_id('catalogue_geometry')).val();
        if (geometry == "light-cone") {
            var number_of_light_cones = parseInt($(lc_id('number_of_light_cones')).val());
            return spinner_check_value(number_of_light_cones);
        }
        return true;
    }

    var validate_number_of_boxes = function() {
        if ($('#max_job_size').hasClass('job_too_large_error')) {
            catalogue.util.show_tab($('#max_job_size'), 0);
            return false;
        } else {
            return true;
        }
    }

    var cleanup_fields = function ($form) {
        // cleanup geometry
        var geometry = vm.catalogue_geometry(); // $(lc_id('catalogue_geometry')).val();
        if (geometry == "box") {
            $('.light_cone_field').val('');
        } else {
            $('.light_box_field').val('');
        }
    }

    function put_handler_ra_and_dec(field_name) {
        var event_handler = function(newValue) {
            var $elem = $(lc_id(field_name));
            if (vm.catalogue_geometry() == "box") {
                clear_error($elem);
                return;
            }
            if (parseFloat(newValue) <= 0. || parseFloat(newValue) > 90.0) {
                set_error($elem, 'Value must be 0 < x <= 90');
            } else {
                clear_error($elem);
            }
            // fill_in_ra_dec_in_summary();
            // The max number of cones should be triggered through a KO dependency
            // calculate_max_number_of_cones();
        }
        clean_inline($(lc_id(field_name)));
        vm[field_name].subscribe(event_handler);
    }

    function init_event_handlers() {

        $('#expand_dataset').click(function (e) {
            e.preventDefault();
            $this = $(this);
            if ($this.html() === "&gt;&gt;") {
                $('div.summary_light_cone .simulation_description, div.summary_light_cone .galaxy_model_description').show();
                $this.html("<<");
            } else {
                $('div.summary_light_cone .simulation_description, div.summary_light_cone .galaxy_model_description').hide();
                $this.html(">>");
            }
            return false;
        });


        $('#expand_output_properties').click(function (e) {
            e.preventDefault();
            $this = $(this);
            if ($this.html() === "&gt;&gt;") {
                $('div.summary_light_cone .output_properties_list').show();
                $this.html("<<");
            } else {
                $('div.summary_light_cone .output_properties_list').hide();
                $this.html(">>");
            }
            return false;
        });

    }


    var empty_light_cone_variables = function () {
        $(lc_id('ra_opening_angle')).attr('value', '');
        $(lc_id('dec_opening_angle')).attr('value', '');
        $(lc_id('redshift_min')).attr('value', '');
        $(lc_id('redshift_max')).attr('value', '');
    }


    var empty_box_variables = function () {
        $(lc_id('box_size')).attr('value', '');
    }


    this.cleanup_fields = function ($form) {
        var geometry = vm.catalogue_geometry(); // $(lc_id('catalogue_geometry')).val();
        if (geometry == 'box') {
            empty_light_cone_variables();
        } else {
            empty_box_variables();
        }
    }


    this.validate = function ($form) {
        return validate_number_of_light_cones() && validate_number_of_boxes();
    }


    this.pre_submit = function ($form) {
        $(lc_id('output_properties') + ' option').each(function (i) {
            $(this).attr("selected", "selected");
        });
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
    
    var galaxy_model_from_dsid = function(dsid) {
    	// Answer the galaxy model for the currently selected dataset
    	debugger;
    	var dsid = vm.dataset();
    	var gmid = catalogue.util.dataset(dsid).fields.galaxy_model;
    	return catalogue.util.galaxy_model(gmid);
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
            { id: 'light_cone', name: 'Light Cone'},
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
        vm.number_of_light_cones = ko.observable(1);
            
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
            if (vm.catalogue_geometry().id == 'light_cone') {
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

        // NOTE: This is a bit nasty because we're mixing jQuery widgets
        // with knouckout observables, but it works.

        $(lc_id('number_of_light_cones')).spinner({
            spin: function (evt, ui) {
                return spinner_check_value(ui.value);
            },
            min: 1
        });

        vm.toggle_light_conne_spinner = ko.computed(function() {
            result = false
            if (vm.light_cone_type() == 'unique') {
                $(lc_id('number_of_light_cones')).spinner("disable");
            } else {
                $(lc_id('number_of_light_cones')).spinner("enable");
                result = true;
            }
            return result;
        });

        return vm;

    }

}
