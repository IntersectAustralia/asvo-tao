
var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};

catalogue.modules.mock_image = function ($) {

    var vm = {}
    this.vm = vm;
	var image_param_names = ['fov_dec', 'fov_ra', 'height',
             'min_mag', 'origin_dec', 'origin_ra', 'width',
             'z_max', 'z_min'];

    function update_apply_mock_image(apply_mock_image) {
        if (apply_mock_image) {
            $('#tao-tabs-3').css({
                "border-style": "solid"
            });
            $('#tao-tabs-3').css({
                "color": "#2BA6CB"
            });

            // Add an image if there is none there.
            if (vm.number_of_images() == 0)
                vm.add_image_settings();

            $('#mock_image_params').slideDown();
            $('#mock_image_info').slideDown();

        } else {
            $('#tao-tabs-3').css({
                "border-style": "dashed"
            });
            $('#tao-tabs-3').css({
                "color": "rgb(119, 221, 252)"
            });

            $('#mock_image_params').slideUp();
            $('#mock_image_info').slideUp();
        }
    }

    this.cleanup_fields = function () {}

    this.validate = function () {
        return true; // TODO !!!
    }

    this.pre_submit = function () {}

    this.job_parameters = function() {
		var max_allowed_images = 1000;
		var image_params;
		var params = {};

		params['mock_image-apply_mock_image'] = [vm.apply_mock_image()];
		params['mock_image-MAX_NUM_FORMS'] = [max_allowed_images];
		params['mock_image-INITIAL_FORMS'] = [0];
		if (vm.apply_mock_image()) {
			image_params = vm.image_settings();
			// Assume that we haven't exceeded the max_allowed_images
			// (which should be checked as part of wizard validation)
			for (var i=0; i<image_params.length; i++) {
				var current_image = image_params[i];
				var key_prefix = 'mock_image-'+ i + '-';

				for (var j=0; j<image_param_names.length; j++) {
					var pn = image_param_names[j];
					params[key_prefix + pn] = [current_image[pn]];
				}
				params[key_prefix + 'format'] = [current_image['format']().value];
				params[key_prefix + 'mag_field'] = [current_image['mag_field']().value];
				params[key_prefix + 'sub_cone'] = [current_image['sub_cone']().value];
			}
			params['mock_image-TOTAL_FORMS']  = [image_params.length];
		} else {
	    	params['mock_image-TOTAL_FORMS'] = [0];
		}
    	return params;
    }

    this.init_model = function (init_params) {
    	// job is either an object containing the job parameters or null
    	var job = init_params.job;
    	var param; // Temporary variable for observable initialisation

        function ImageParameters(prefix, job) {
            var def = catalogue.validators.defined;
            var image_params = {};
            var param;
            
            function get_param(prefix, pn) {
            	var res;

            	// If no prefix is provided, return negative
            	if (prefix == undefined || prefix == null || prefix == "") {
            		return false;
            	}
            	// But if a prefix is supplied, the parameter is mandatory
            	res = job[prefix+pn];
            	if (res == undefined) throw "mock_image missing parameter: " + prefix + pn;
            	return res;
            }


            param = get_param(prefix, '-sub_cone');
            param = catalogue.util.get_observable_by_attribute('value', param, vm.sub_cone_options);
            image_params.sub_cone = ko.observable(param ? param : vm.sub_cone_options()[0]);

            // vm.sub_cone_options.subscribe(function(arr){
            //     var sc_value = image_params.sub_cone().value;
            //     var new_obj;
            //     for(var i=0; i<arr.length; i++) {
            //         if (arr[i].value == sc_value) {
            //             new_obj = arr[i];
            //             break;
            //         }
            //     }
            //     console.log(new_obj);
            //     if (new_obj !== image_params.sub_cone()) {
            //         image_params.sub_cone(new_obj);
            //     }
            // });
            
            vm.sub_cone_options.subscribe(function(arr){
                var new_obj = catalogue.util.get_observable_by_attribute('value', image_params.sub_cone().value, vm.sub_cone_options);
                if (new_obj !== image_params.sub_cone()) {
                    image_params.sub_cone(new_obj);
                }
            });

            param = get_param(prefix, '-format');
            param = catalogue.util.get_element_by_attribute('value', param, vm.format_options);
            image_params.format = ko.observable(param ? param : vm.format_options[0]);

            image_params.mag_field_options = ko.computed(function(){
                return catalogue.modules.sed.vm.bandpass_filters.to_side.options();
            });
            param = get_param(prefix, '-mag_field');
            param = catalogue.util.get_observable_by_attribute('value', param, image_params.mag_field_options);
            image_params.mag_field = ko.observable(param ? param : mag_field_options[0]);

            param = get_param(prefix, '-fov_ra');
            image_params.fov_ra = ko.observable(param ? param : catalogue.modules.light_cone.vm.ra_opening_angle());
            param = get_param(prefix, '-fov_dec');
            image_params.fov_dec = ko.observable(param ? param : catalogue.modules.light_cone.vm.dec_opening_angle());
            param = get_param(prefix, '-width');
            image_params.width = ko.observable(param ? param : 1024)
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.geq(1)})
                .extend({validate: catalogue.validators.leq(4096)});
            param = get_param(prefix, '-height');
            image_params.height = ko.observable(param ? param : 1024)
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.geq(1)})
                .extend({validate: catalogue.validators.leq(4096)});
            param = get_param(prefix, '-min_mag');
            image_params.min_mag = ko.observable(param ? param : 7)
                .extend({validate: catalogue.validators.is_float});
            param = get_param(prefix, '-z_min');
            image_params.z_min = ko.observable(param ? param : catalogue.modules.light_cone.vm.redshift_min())
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.geq(
                    catalogue.modules.light_cone.vm.redshift_min
                    )})
                .extend({validate: catalogue.validators.leq(
                    catalogue.modules.light_cone.vm.redshift_max
                    )});
            param = get_param(prefix, '-z_max');
            image_params.z_max = ko.observable(param ? param : catalogue.modules.light_cone.vm.redshift_max())
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.geq(
                    catalogue.modules.light_cone.vm.redshift_min
                    )})
                .extend({validate: catalogue.validators.leq(
                    catalogue.modules.light_cone.vm.redshift_max
                    )})
                .extend({validate: catalogue.validators.greater_than(
                    image_params.z_min
                )});
            param = get_param(prefix, '-origin_ra');
            image_params.origin_ra = ko.observable(param ? param :
                    (def(catalogue.modules.light_cone.vm.ra_opening_angle()) ?
                    catalogue.modules.light_cone.vm.ra_opening_angle()/2 : ''));
            image_params.origin_ra
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.test(
                    ko.computed(function(){
                        if (!def(image_params.fov_ra())
                            || !def(catalogue.modules.light_cone.vm.ra_opening_angle()))
                            return true;
                        return parseFloat(image_params.origin_ra()) + 0.5 * parseFloat(image_params.fov_ra())
                            <= parseFloat(catalogue.modules.light_cone.vm.ra_opening_angle());
                    }),
                    "Origin and field-of-view RAs exceed cone maximum."
                )})
                .extend({validate: catalogue.validators.test(
                    ko.computed(function(){
                        if (!def(image_params.fov_ra()))
                            return true;
                        return parseFloat(image_params.origin_ra()) - 0.5 * parseFloat(image_params.fov_ra()) >= 0.0;
                    }),
                    "Origin and field-of-view RAs are below cone minimum."
                )});
            param = get_param(prefix, '-origin_dec');
            image_params.origin_dec = ko.observable(param ? param :
                    (def(catalogue.modules.light_cone.vm.dec_opening_angle()) ?
                        catalogue.modules.light_cone.vm.dec_opening_angle()/2 : ''));
            image_params.origin_dec
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.test(
                    ko.computed(function(){
                        if (!def(image_params.fov_dec())
                            || !def(catalogue.modules.light_cone.vm.dec_opening_angle()))
                            return true;
                        return parseFloat(image_params.origin_dec()) + 0.5 * parseFloat(image_params.fov_dec())
                            <= parseFloat(catalogue.modules.light_cone.vm.dec_opening_angle());
                    }),
                    "Origin and field-of-view DECs exceed cone maximum.")})
                .extend({validate: catalogue.validators.test(
                    ko.computed(function(){
                        if (!def(image_params.fov_dec()))
                            return true;
                        return parseFloat(image_params.origin_dec()) - 0.5 * parseFloat(image_params.fov_dec()) >= 0.0;
                    }),
                    "Origin and field-of-view DECs are below cone minimum."
                )});

            return image_params;
        }
        
        function add_images_from(job) {
        	// Add the images from the supplied job parameters
        	var num_images;

        	if (!vm.apply_mock_image()) return;
        	
        	num_images = parseInt(job['mock_image-INITIAL_FORMS']);
        	if (isNaN(num_images)) return;
        	for (var i=0; i<num_images; i++) {
        		var prefix = 'mock_image' + i;
        		vm.image_settings.push(ImageParameters(prefix, job));
        	}
        }

        vm.add_image_settings = function() {
            var params = ImageParameters();
            vm.image_settings.push(params);
        }

        vm.remove_image_settings = function(obj) {
            vm.image_settings.remove(obj);
            if (vm.image_settings().length == 0)
                vm.add_image_settings();
        }

        vm.can_have_images = ko.computed(function(){
            return catalogue.modules.sed.vm.apply_sed() &&
                catalogue.modules.light_cone.vm.catalogue_geometry().id == 'light-cone' &&
                catalogue.modules.sed.vm.bandpass_filters.to_side.options().length > 0;
        });

        param = job['mock_image-apply_mock_image']
        vm.apply_mock_image = ko.observable(param ? param : false);

        vm.apply_mock_image.subscribe(function(val){
            update_apply_mock_image(val, vm);
        });

        vm.image_settings = ko.observableArray([]);

        vm.sub_cone_options = ko.computed(function(){
            console.log('sub_cone_options CALLED!');
            var n = catalogue.modules.light_cone.vm.number_of_light_cones();
            var resp = [{value: 'ALL', text:'All'}]
            for(var i = 1; i<=n; i++)
                resp.push({value:i, text:i});
            return resp;
        });

        vm.format_options = [
                {value:'FITS', text:'FITS'}
                // png and jpg formats aren't working yet
                // {value:'PNG', text:'PNG'},
                // {value:'JPEG', text:'JPEG'}
        ];

        add_images_from(job);

        vm.number_of_images = ko.computed(function() {
            return vm.image_settings().length;
        });

        return vm;

    }

}
