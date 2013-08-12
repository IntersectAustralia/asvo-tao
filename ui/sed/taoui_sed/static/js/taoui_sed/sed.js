
var catalogue = catalogue || {}
catalogue.modules = catalogue.modules || {}


catalogue.modules.sed = function ($) {

    this.sed_band_pass_filters_widget = null;

    function get_widget() {
        return catalogue.modules.sed.sed_band_pass_filters_widget;
    }


    function display_band_pass_filters_summary() {
        var band_pass_filter_count = catalogue.util.list_multiple_selections_in_summary('sed', 'band_pass_filters');
        if (band_pass_filter_count == 1)
            catalogue.util.fill_in_summary('sed', 'band_pass_filters', band_pass_filter_count + " filter selected");
        else
            catalogue.util.fill_in_summary('sed', 'band_pass_filters', band_pass_filter_count + " filters selected");
    }


    var show_dust_model_info = function (dust_id) {
        data = catalogue.util.dust_model(dust_id);
        $('div.dust-model-info .name').html(data.fields.name);
        $('div.dust-model-info .details').html(data.fields.details);
        $('div.dust-model-info').show();
        catalogue.util.fill_in_summary('sed', 'dust_model', data.fields.name);
        catalogue.util.fill_in_summary('sed', 'dust_model_description', '<br>' + data.fields.details);
        // $.ajax({
        //     url: TAO_JSON_CTX + 'dust_model/' + dust_id,
        //     dataType: "json",
        //     error: function () {
        //         $('div.dust-model-info').hide();
        //         alert("Couldn't get data for requested dust model");
        //     },
        //     success: function (data, status, xhr) {
        //         $('div.dust-model-info .name').html(data.fields.name);
        //         $('div.dust-model-info .details').html(data.fields.details);
        //         $('div.dust-model-info').show();
        //         catalogue.util.fill_in_summary('sed', 'dust_model', data.fields.name);
        //         catalogue.util.fill_in_summary('sed', 'dust_model_description', '<br>' + data.fields.details);
        //     }
        // });
    };


    function init_bandpass_properties() {
        var current = [];
        $(sed_id('band_pass_filters') + ' option').each(function () {
            var $this = $(this);
            if ($this.attr('selected')) {
                current.push($this.attr('value'));
            }
        });
        data = catalogue.util.bandpass_filters();
        get_widget().cache_store(data);
        catalogue.modules.record_filter.update_filter_options.bandpass_props = true;
        get_widget().display_selected(current, true);
        // $.ajax({
        //     url: TAO_JSON_CTX + 'bandpass_filters/',
        //     dataType: "json",
        //     error: function (jqXHR, status, error) {
        //         alert("Couldn't get bandpass filters");
        //     },
        //     success: function (data, status, xhr) {
        //         get_widget().cache_store(data);
        //         catalogue.modules.record_filter.update_filter_options.bandpass_props = true;
        //         get_widget().display_selected(current, true);
        //     }
        // });
        console.log('Current bandpass filters: ' + current);
        return current;
    }


    function show_bandpass_filter_info(cache_item) {
        $('div.band-pass-info .name').html(cache_item.text);
        $('div.band-pass-info .details').html(cache_item.description);
        $('div.band-pass-info').show();
    }


    function init_event_handlers() {
        $('#expand_stellar_model').click(function (e) {
            e.preventDefault();
            $this = $(this);
            if ($this.html() === "&gt;&gt;") {
                $('div.summary_sed .stellar_model_description').show();
                $this.html("<<");
            } else {
                $('div.summary_sed .stellar_model_description').hide();
                $this.html(">>");
            }
            return false;
        });


        $('#expand_dust_model').click(function (e) {
            e.preventDefault();
            $this = $(this);
            if ($this.html() === "&gt;&gt;") {
                $('div.summary_sed .dust_model_description').show();
                $this.html("<<");
            } else {
                $('div.summary_sed .dust_model_description').hide();
                $this.html(">>");
            }
            return false;
        });


        $('#expand_band_pass_filters').click(function (e) {
            e.preventDefault();
            $this = $(this);
            if ($this.html() === "&gt;&gt;") {
                $('div.summary_sed .band_pass_filters_list').show();
                $this.html("<<");
            } else {
                $('div.summary_sed .band_pass_filters_list').hide();
                $this.html(">>");
            }
            return false;
        });


        $(sed_id('select_dust_model')).change(function (evt) {
            var $this = $(this);
            var dust_id = $this.val();
            show_dust_model_info(dust_id);
        });


        $(sed_id('band_pass_filters_add_link')).change(function () {
            catalogue.util.fill_in_summary('sed', 'band_pass_filters', 'band_pass_filters_add_link.click()');
            $(sed_id('band_pass_filters_to')).change();
        });


        $(sed_id('band_pass_filters_remove_link')).click(function () {
            $(sed_id('band_pass_filters_to')).change();
        });


        $(sed_id('band_pass_filters_add_all_link')).click(function (evt) {
            catalogue.util.fill_in_summary('sed', 'band_pass_filters', 'band_pass_filters_add_all_link.click()');
            $(sed_id('band_pass_filters_to')).change();
        });


        $(sed_id('band_pass_filters_remove_all_link')).click(function () {
            $(sed_id('band_pass_filters_to')).change();
        });


        $(sed_id('single_stellar_population_model')).change(function (evt) {
            var $this = $(this);
            catalogue.util.show_stellar_model_info($this.val())
            var single_stellar_population_model_value = $this.find('option:selected').html();
            catalogue.util.fill_in_summary('sed', 'single_stellar_population_model', single_stellar_population_model_value);
        });


        $(sed_id('apply_dust')).change(function (evt) {
            if ($(sed_id('apply_dust')).is(':checked')) {
                $(sed_id('select_dust_model')).removeAttr('disabled');
                $(sed_id('select_dust_model')).change();
                $('#expand_dust_model').show();
            } else {
                $(sed_id('select_dust_model')).attr('disabled', 'disabled');
                catalogue.util.clear_info('sed', 'dust-model');
                catalogue.util.clear_in_summary('sed', 'dust_model');
                $('#expand_dust_model').hide();
                $('div.summary_sed .dust_model_description').hide();
            }
        });


        $(sed_id('apply_sed')).change(function (evt) {
            if ($(sed_id('apply_sed')).is(':checked')) {
                $('#tao-tabs-2').css({
                    "border-style": "solid"
                });
                $('#tao-tabs-2').css({
                    "color": "#2BA6CB"
                });
                $(sed_id('single_stellar_population_model')).removeAttr('disabled');
                $(sed_id('single_stellar_population_model')).change();
                $(sed_id('band_pass_filters_filter')).removeAttr('disabled');
                $(sed_id('band_pass_filters_from')).removeAttr('disabled');
                get_widget().set_enabled(true);
                $(sed_id('band_pass_filters')).removeAttr('disabled');
                $('div.summary_sed .apply_sed').show();
                catalogue.util.fill_in_summary('sed', 'select_sed', '');
                display_band_pass_filters_summary();
                $(sed_id('apply_dust')).removeAttr('disabled');
                $(sed_id('apply_dust')).change();
                catalogue.modules.record_filter.update_filter_options(); // triggers filter.change
                $('#sed_params').slideDown();
                $('#sed_info').slideDown();
            } else {
                $('#tao-tabs-2').css({
                    "border-style": "dashed"
                });
                $('#tao-tabs-2').css({
                    "color": "rgb(119, 221, 252)"
                });
                $(sed_id('single_stellar_population_model')).attr('disabled', 'disabled');
                catalogue.util.clear_in_summary('sed', 'single_stellar_population_model');
                $(sed_id('band_pass_filters_filter')).attr('disabled', 'disabled');
                $(sed_id('band_pass_filters_from')).attr('disabled', 'disabled');
                get_widget().set_enabled(false);
                $(sed_id('band_pass_filters')).attr('disabled', 'disabled');
                catalogue.util.clear_in_summary('sed', 'band_pass_filters');
                $(sed_id('apply_dust')).attr('disabled', 'disabled');
                $(sed_id('select_dust_model')).attr('disabled', 'disabled');
                catalogue.util.clear_info('sed', 'stellar-model');
                catalogue.util.clear_info('sed', 'band-pass');
                catalogue.util.clear_info('sed', 'dust-model');
                $('div.summary_sed .apply_sed').hide();
                catalogue.util.fill_in_summary('sed', 'select_sed', 'Not selected');
                catalogue.modules.record_filter.update_filter_options(); // triggers filter.change
                $('#sed_params').slideUp();
                $('#sed_info').slideUp();
            }
        });


        get_widget().change_event(function (evt) {
            catalogue.modules.record_filter.update_filter_options();
            display_band_pass_filters_summary();
        });


        get_widget().option_clicked_event(function (cache_item) {
            show_bandpass_filter_info(cache_item);
        });

    }


    this.cleanup_fields = function ($form) {}


    this.validate = function ($form) {
        return true;
    }


    this.pre_submit = function ($form) {
        $(sed_id('band_pass_filters') + ' option').each(function (i) {
            $(this).attr("selected", "selected");
        });
    }

    function band_pass_filter_to_option(bpf) {
        return {
            'value': bpf.pk,
            'text' : bpf.fields.label,
            'group': bpf.fields.group
        }
    }

    this.init_model = function () {

        var vm = {}
        this.vm = vm

        vm.apply_sed = ko.observable(false);

        this.sed_band_pass_filters_widget = TwoSidedSelectWidget(sed_id('band_pass_filters'),
            {'selected':[],'not_selected':[]}, band_pass_filter_to_option);
        this.sed_band_pass_filters_widget.init();

        var current_bandpass = init_bandpass_properties();

        init_event_handlers();

        $(sed_id('apply_sed')).change();
        $(sed_id('apply_dust')).change();

        $('div.summary_sed .band_pass_filters_list').hide();
        $('div.summary_sed .stellar_model_description').hide();
        $('div.summary_sed .dust_model_description').hide();

        setTimeout(function () {
            display_band_pass_filters_summary()
        }, 1000);

        return vm;

    }

}