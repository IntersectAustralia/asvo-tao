
var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};

catalogue.modules.mock_image = function ($) {

//    function mock_image_enabled() {
//        var ami = $('#id_mock_image-apply_mock_image');
//        return ami.attr('disabled') === undefined && ami.is(':checked');
//    }
//

    function mock_image_setup_form_behaviors(form) {

        //
        // Setup validation on each input.
        //

        // sub_cone
        form.find('select[name$="sub_cone"]').validate({
            required: true,
            form: 'mock_image'
        });

        // format
        form.find('select[name$="format"]').validate({
            required: true,
            form: 'mock_image'
        });

        // mag_field
        form.find('select[name$="mag_field"]').validate({
            required: true,
            form: 'mock_image'
        });

        // z_min
        form.find('input[name$="z_min"]').validate({
            type: 'float',
            required: true,
            cache: {
                z_min: [$('#id_light_cone-redshift_min'), 'float'],
                z_max: [$('#id_light_cone-redshift_max'), 'float']
            },
            group: [form.find('input[name$="z_max"]')],
            form: 'mock_image'
        }).validate('test', {
            check: function (val, cache) {
                return val >= cache.z_min;
            },
            message: ['Value must be greater than the minimum redshift of ',
                'the cone specified in General Properties.'
            ].join('')
        }).validate('test', {
            check: function (val, cache) {
                return val <= cache.z_max;
            },
            message: ['Value must be less than the maximum redshift of ',
                'the cone specified in General Properties.'
            ].join('')
        }).validate('test', {
            check: function (val, cache) {
                return val <= form.find('input[name$="z_max"]').val();
            },
            message: ['Value must be less than the maximum redshift of ',
                'this mock image.'
            ].join('')
        });

        // z_max
        form.find('input[name$="z_max"]').validate({
            type: 'float',
            required: true,
            cache: {
                z_min: [$('#id_light_cone-redshift_min'), 'float'],
                z_max: [$('#id_light_cone-redshift_max'), 'float']
            },
            group: [form.find('input[name$="z_min"]')],
            form: 'mock_image'
        }).validate('test', {
            check: function (val, cache) {
                return val <= cache.z_max;
            },
            message: ['Value must be less than the maximum redshift of ',
                'the cone specified in General Properties.'
            ].join('')
        }).validate('test', {
            check: function (val, cache) {
                return val >= cache.z_min;
            },
            message: ['Value must be greater than the minimum redshift of ',
                'the cone specified in General Properties.'
            ].join('')
        }).validate('test', {
            check: function (val, cache) {
                return val >= form.find('input[name$="z_min"]').val();
            },
            message: ['Value must be greater than the minimum redshift of ',
                'this mock image.'
            ].join('')
        });

        // origin_ra
        form.find('input[name$="origin_ra"]').validate({
            type: 'float',
            required: true,
            cache: {
                ra: [$('#id_light_cone-ra_opening_angle'), 'float'],
                fov_ra: [form.find('input[name$="fov_ra"]'), 'float']
            },
            group: [form.find('input[name$="fov_ra"]')],
            form: 'mock_image'
        }).validate('test', {
            check: function (val, cache) {
                return val + 0.5 * cache.fov_ra <= cache.ra;
            },
            message: 'Origin and field-of-view RAs exceed cone maximum.'
        }).validate('test', {
            check: function (val, cache) {
                return val - 0.5 * cache.fov_ra >= 0;
            },
            message: 'Origin and field-of-view RAs are below cone minimum.'
        });

        // origin_dec
        form.find('input[name$="origin_dec"]').validate({
            type: 'float',
            required: true,
            cache: {
                dec: [$('#id_light_cone-dec_opening_angle'), 'float'],
                fov_dec: [form.find('input[name$="fov_dec"]'), 'float']
            },
            group: [form.find('input[name$="fov_dec"]')],
            form: 'mock_image'
        }).validate('test', {
            check: function (val, cache) {
                return val + 0.5 * cache.fov_dec <= cache.dec;
            },
            message: 'Origin and field-of-view DECs exceed cone maximum.'
        }).validate('test', {
            check: function (val, cache) {
                return val - 0.5 * cache.fov_dec >= 0;
            },
            message: 'Origin and field-of-view DECs are below cone minimum.'
        });

        // fov_ra
        form.find('input[name$="fov_ra"]').validate({
            type: 'float',
            required: true,
            cache: {
                ra: [$('#id_light_cone-ra_opening_angle'), 'float'],
                o_ra: [form.find('input[name$="origin_ra"]'), 'float']
            },
            group: [form.find('input[name$="origin_ra"]')],
            form: 'mock_image'
        }).validate('test', {
            check: function (val, cache) {
                return cache.o_ra + 0.5 * val <= cache.ra;
            },
            message: 'Origin and field-of-view RAs exceed cone maximum.'
        }).validate('test', {
            check: function (val, cache) {
                return cache.o_ra - 0.5 * val >= 0;
            },
            message: 'Origin and field-of-view RAs are below cone minimum.'
        });

        // fov_dec
        form.find('input[name$="fov_dec"]').validate({
            type: 'float',
            required: true,
            cache: {
                dec: [$('#id_light_cone-dec_opening_angle'), 'float'],
                o_dec: [form.find('input[name$="origin_dec"]'), 'float']
            },
            group: [form.find('input[name$="origin_dec"]')],
            form: 'mock_image'
        }).validate('test', {
            check: function (val, cache) {
                return cache.o_dec + 0.5 * val <= cache.dec;
            },
            message: 'Origin and field-of-view DECs exceed cone maximum.'
        }).validate('test', {
            check: function (val, cache) {
                return cache.o_dec - 0.5 * val >= 0;
            },
            message: 'Origin and field-of-view DECs are below cone minimum.'
        });

        // width
        form.find('input[name$="width"]').validate({
            type: 'int',
            required: true,
            form: 'mock_image'
        }).validate('test', {
            check: function (val) {
                return val > 1;
            },
            message: 'Image must have at least 1 pixel in width.'
        }).validate('test', {
            check: function (val) {
                return val < 4096;
            },
            message: 'Maximum image width is 4096 pixels.'
        });

        // height
        form.find('input[name$="height"]').validate({
            type: 'int',
            required: true,
            form: 'mock_image'
        }).validate('test', {
            check: function (val) {
                return val > 1;
            },
            message: 'Image must have at least 1 pixel in height.'
        }).validate('test', {
            check: function (val) {
                return val < 4096;
            },
            message: 'Maximum image height is 4096 pixels.'
        });
    }

    function mock_image_setup_form(form) {
        var ra = $('#id_light_cone-ra_opening_angle').val();
        var dec = $('#id_light_cone-dec_opening_angle').val();
        var z_min = $('#id_light_cone-redshift_min').val();
        var z_max = $('#id_light_cone-redshift_max').val();
        // update_mock_image_sub_cones(form.find('select[name$="sub_cone"]'));
        mock_image_update_magnitudes(form.find('select[name$="mag_field"]'));
        form.find('input[name$="min_mag"]').val(7);
        form.find('input[name$="z_min"]').val(z_min);
        form.find('input[name$="z_max"]').val(z_max);
        if (ra != "") {
            form.find('input[name$="origin_ra"]').val(ra / 2.0);
            form.find('input[name$="fov_ra"]').val(ra);
        }
        if (dec !== "") {
            form.find('input[name$="origin_dec"]').val(dec / 2.0);
            form.find('input[name$="fov_dec"]').val(dec);
        }
        form.find('input[name$="width"]').val(1024);
        form.find('input[name$="height"]').val(1024);

        $('.delete-row:last').click(function () {
            return true;
        });

        mock_image_setup_form_behaviors(form);
    }

    function update_apply_mock_image(apply_mock_image, vm) {
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

            // if ($('#mock_image_params .single-form').length == 0)
            //    $('#mock_image_params .add-row').click();

            // Enable all inputs except hidden ones.
            // $('#mock_image_params input[type!="hidden"], #mock_image_params select').removeAttr('disabled');

            $('#mock_image_params').slideDown();
            $('#mock_image_info').slideDown();

        } else {
            $('#tao-tabs-3').css({
                "border-style": "dashed"
            });
            $('#tao-tabs-3').css({
                "color": "rgb(119, 221, 252)"
            });

            // Disable all inputs except hidden ones.
            // $('#mock_image_params input[type!="hidden"], #mock_image_params select').attr('disabled', 'disabled');

            $('#mock_image_params').slideUp();
            $('#mock_image_info').slideUp();
        }
    }


    function mock_image_update_magnitudes(sel) {
        if (sel === undefined)
            sel = $('#mock_image_params select[name$="mag_field"]');
        // update_select(sel, $('#id_sed-band_pass_filters > option'));
    }


//    function update_mock_image_sub_cones(sel) {
//        if (sel === undefined)
//            sel = $('#mock_image_params select[name$="sub_cone"]');
//        var num_cones = parseInt($('#id_light_cone-number_of_light_cones').val());
//        sel.each(function () {
//            var cur = $(this).children('option:selected').attr('value');
//            $(this).empty();
//            $(this).append($('<option/>').attr('value', 'ALL').text('All'));
//            if (num_cones !== undefined && num_cones > 1) {
//                for (var ii = 0; ii < num_cones; ii++) {
//                    var opt = $('<option/>').attr('value', ii).text(ii);
//                    if (opt.attr('value') == cur)
//                        opt.prop('selected', true);
//                    $(this).append(opt);
//                }
//            }
//        });
//    }


//    function update_select(sel, opts) {
//        sel.each(function () {
//            var cur_sel = $(this);
//            var cur_opt = cur_sel.children('option:selected').attr('value');
//            cur_sel.empty();
//            opts.each(function () {
//                var opt = $('<option/>').attr('value', $(this).attr('value')).text($(this).text());
//                if ($(this).attr('value') == cur_opt)
//                    opt.prop('selected', true);
//                cur_sel.append(opt);
//            });
//            cur_sel.change();
//        });
//    }


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


    this.init_model = function () {

        var vm = {}
        this.vm = vm;

        function ImageParameters() {
            var image_params = {};
            image_params.sub_cone = ko.observable(vm.sub_cone_options()[0]);
            image_params.format = ko.observable(vm.format_options[0]);
            image_params.mag_field_options = ko.computed(function(){
                // TODO, should link to SED
                return catalogue.util.bandpass_filters();
            });
            image_params.mag_field = ko.observable();
            image_params.min_mag = ko.observable()
                .extend({logger: 'min_max'})
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.positive});
            image_params.z_min = ko.observable()
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.greater_than(
                    catalogue.modules.light_cone.vm.redshift_min
                    )})
                .extend({validate: catalogue.validators.less_than(
                    catalogue.modules.light_cone.vm.redshift_max
                    )})
            image_params.z_max = ko.observable()
                .extend({validate: catalogue.validators.is_float})
                .extend({validate: catalogue.validators.greater_than(
                    catalogue.modules.light_cone.vm.redshift_min
                    )})
                .extend({validate: catalogue.validators.less_than(
                    catalogue.modules.light_cone.vm.redshift_max
                    )})
                .extend({validate: catalogue.validators.greater_than(
                    image_params.z_min
                )})
            image_params.origin_ra = ko.observable();
            image_params.origin_dec = ko.observable();
            image_params.fov_ra = ko.observable();
            image_params.fov_dec = ko.observable();
            image_params.width = ko.observable();
            image_params.height = ko.observable();
            return image_params;
        }

        vm.can_have_images = ko.computed(function(){
            return catalogue.modules.sed.vm.apply_sed() &&
                catalogue.modules.light_cone.vm.catalogue_geometry().id == 'light_cone';
        });

        vm.sub_cone_options = ko.computed(function(){
            var n = catalogue.modules.light_cone.vm.number_of_light_cones();
            var resp = [{value: 'ALL', text:'All'}]
            for(var i = 1; i<=n; i++)
                resp.push({value:i, text:i});
            return resp;
        });

        vm.format_options = [
                {value:'FITS', text:'FITS'},
                {value:'PNG', text:'PNG'},
                {value:'JPEG', text:'JPEG'}
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

        // TODO: perhaps move the event handlers to init_event_handlers()
        // to be consistent with other modules

        // $('#mock_image_params .single-form').formset({
        //     prefix: 'mock_image'
        // });

        // We always have an extra form at the end, so delete it
        // now that we've initialised the formset.
        // $('#mock_image_params .single-form:last').remove();
        $('#id_mock_image-TOTAL_FORMS').val(parseInt($('#id_mock_image-TOTAL_FORMS').val()) - 1);

        // Pretty up the "add another" button and add my own click handler.
        $('.add-row').button().click(function () {
            mock_image_setup_form($('#mock_image_params .single-form:last'));
            return true;
        });

        // Add behaviors to existing forms.
        // $('#mock_image_params .single-form').each(function () {
        //     mock_image_setup_form_behaviors($(this));
        // });

        // Run validation on all existing forms. Don't force anything here,
        // as we don't know if this is a returning form or a new one. If it's
        // returning, then any errors flagged in control groups will be picked
        // up by jQuery.validate.
        // $('#mock_image_params .single-form').each(function () {
        //     $.validate_form('mock_image');
        // });

        // Reevaluate all the magnitude fields.
        // mock_image_update_magnitudes();

        return vm;

    }

}
