
var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};

catalogue.modules.mock_image = function ($) {

    var vm = {}
    this.vm = vm;

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

    this.update_tabs = function (event, ui) {
        var old_tab = $(ui.oldTab).children('a:first').attr('id');
        var new_tab = $(ui.newTab).children('a:first').attr('id');

        // Check if the mock-image tab should be enabled.
        if (old_tab == 'tao-tabs-1' || old_tab == 'tao-tabs-2') {
            var sel = $('#id_light_cone-catalogue_geometry option:selected').val();
            if ($('#id_light_cone-catalogue_geometry option:selected').val() == 'light-cone' &&
                $('#id_sed-apply_sed').is(':checked')) {
                $(mi_id('apply_mock_image')).removeAttr('disabled');
                update_apply_mock_image();
            } else {
                $(mi_id('apply_mock_image')).attr('disabled', 'disabled');
                update_apply_mock_image();
            }
        }

        // Update all mock image magnitudes.
        if (old_tab == 'tao-tabs-2')
            mock_image_update_magnitudes();

        // Update every mock image sub-cone option with appropriate
        // values from the general properties.
        // if (old_tab == 'tao-tabs-1')
        //    update_mock_image_sub_cones();

        // Upon moving to a new tab, run validation in the tab to pick up
        // any changes from previous tab.
        if (new_tab == 'tao-tabs-3')
            $.validate_form('mock_image');
    }

    this.cleanup_fields = function ($form) {}


    this.validate = function ($form) {
        return $.validate_all(true) == undefined;
    }


    this.pre_submit = function ($form) {}

    this.job_parameters = function() {
		var max_allowed_images = 1000;
		var image_params;
		var params = {};
		var param_names = ['fov_dec', 'fov_ra', 'height',
		    'min_mag', 'origin_dec', 'origin_ra', 'width',
		    'z_max', 'z_min'];

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

				for (var j=0; j<param_names.length; j++) {
					var pn = param_names[j];
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

    this.init_model = function () {

        function ImageParameters() {
            var def = catalogue.validators.defined;
            var image_params = {};
            image_params.sub_cone = ko.observable(vm.sub_cone_options()[0]);
            image_params.format = ko.observable(vm.format_options[0]);
            image_params.mag_field_options = ko.computed(function(){
                return catalogue.modules.sed.vm.bandpass_filters.to_side.options();
            });
            image_params.mag_field = ko.observable();
            image_params.fov_ra = ko.observable(catalogue.modules.light_cone.vm.ra_opening_angle());
            image_params.fov_dec = ko.observable(catalogue.modules.light_cone.vm.dec_opening_angle());
            image_params.width = ko.observable(1024)
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.geq(1)})
                .extend({validate: catalogue.validators.leq(4096)});
            image_params.height = ko.observable(1024)
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.geq(1)})
                .extend({validate: catalogue.validators.leq(4096)});
            image_params.min_mag = ko.observable(7)
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.positive});
            image_params.z_min = ko.observable(catalogue.modules.light_cone.vm.redshift_min())
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.geq(
                    catalogue.modules.light_cone.vm.redshift_min
                    )})
                .extend({validate: catalogue.validators.leq(
                    catalogue.modules.light_cone.vm.redshift_max
                    )});
            image_params.z_max = ko.observable(catalogue.modules.light_cone.vm.redshift_max())
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
            image_params.origin_ra = ko.observable(
                    def(catalogue.modules.light_cone.vm.ra_opening_angle()) ?
                    catalogue.modules.light_cone.vm.ra_opening_angle()/2 : '');
            image_params.origin_ra
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.test(
                    ko.computed(function(){
                        if (!def(image_params.fov_ra())
                            || !def(catalogue.modules.light_cone.vm.ra_opening_angle()))
                            return true;
                        return image_params.origin_ra() + 0.5 * image_params.fov_ra()
                            <= catalogue.modules.light_cone.vm.ra_opening_angle();
                    }),
                    "Origin and field-of-view RAs exceed cone maximum."
                )})
                .extend({validate: catalogue.validators.test(
                    ko.computed(function(){
                        if (!def(image_params.fov_ra()))
                            return true;
                        return image_params.origin_ra() - 0.5 * image_params.fov_ra() >= 0.0;
                    }),
                    "Origin and field-of-view RAs are below cone minimum."
                )});
            image_params.origin_dec = ko.observable(
                    def(catalogue.modules.light_cone.vm.ra_opening_angle()) ?
                        catalogue.modules.light_cone.vm.ra_opening_angle()/2 : '');
            image_params.origin_dec
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.test(
                    ko.computed(function(){
                        if (!def(image_params.fov_dec())
                            || !def(catalogue.modules.light_cone.vm.dec_opening_angle()))
                            return true;
                        return image_params.origin_dec() + 0.5 * image_params.fov_dec()
                            <= catalogue.modules.light_cone.vm.dec_opening_angle();
                    }),
                    "Origin and field-of-view DECs exceed cone maximum.")})
                .extend({validate: catalogue.validators.test(
                    ko.computed(function(){
                        if (!def(image_params.fov_dec()))
                            return true;
                        return image_params.origin_dec() - 0.5 * image_params.fov_dec() >= 0.0;
                    }),
                    "Origin and field-of-view DECs are below cone minimum."
                )});

            return image_params;
        }

        vm.can_have_images = ko.computed(function(){
            return catalogue.modules.sed.vm.apply_sed() &&
                catalogue.modules.light_cone.vm.catalogue_geometry().id == 'light-cone' &&
                catalogue.modules.sed.vm.bandpass_filters.to_side.options().length > 0;
        });

        vm.sub_cone_options = ko.computed(function(){
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

        vm.apply_mock_image = ko.observable(false);

        vm.apply_mock_image.subscribe(function(val){
            update_apply_mock_image(val, vm);
        });

        vm.image_settings = ko.observableArray([]);

        vm.number_of_images = ko.computed(function() {
             return vm.image_settings().length;
        });

        vm.add_image_settings = function() {
            var params = ImageParameters();
            vm.image_settings.push(params);
        }

        vm.remove_image_settings = function(obj) {
            vm.image_settings.remove(obj);
            if (vm.image_settings().length == 0)
                vm.add_image_settings();
        }

        // We always have an extra form at the end, so delete it
        // now that we've initialised the formset.
        // $('#mock_image_params .single-form:last').remove();
        $('#id_mock_image-TOTAL_FORMS').val(parseInt($('#id_mock_image-TOTAL_FORMS').val()) - 1);

        return vm;

    }

}
