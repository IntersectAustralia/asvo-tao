jQuery(document).ready(function($) {

    var lc_id = function(bare_name) {
        return '#id_light_cone-' + bare_name;
    };

    var sed_id = function(bare_name) {
        return '#id_sed-' + bare_name;
    };

    var rf_id = function(bare_name) {
        return '#id_record_filter-' + bare_name;
    }

    var item_to_value = function(item) {
        return item.type + '-' + item.pk;
    }

    // focus on tab (direction=0), next tab (direction=+1) or prev tab (direction=-1)
    var show_tab = function($elem, direction) {
        var this_tab = parseInt($elem.closest('div.tao-tab').attr('tao-number'));
        $('#tao-tabs-' + (this_tab + direction)).click();
    }

    var show_error = function($field, msg) {
        var $enclosing = $field.closest('div.control-group');
        $enclosing.find('span.help-inline').remove();
        $enclosing.removeClass('error');
        if (msg == null) return;
        $field.after('<span class="help-inline"></span>');
        $enclosing.find('span.help-inline').text(msg);
        $enclosing.addClass('error');
        show_tab($enclosing, 0);
    }

    var lc_output_props_widget = new TwoSidedSelectWidget(lc_id('output_properties'), true);

    var sed_band_pass_filters_widget = new TwoSidedSelectWidget(sed_id('band_pass_filters'), false);

    var display_band_pass_filters_summary = function() {
        var band_pass_filter_values = [];
        band_pass_filter_values.push('<ul>');
        $(sed_id('band_pass_filters')+' option').each(function(i) {
            band_pass_filter_values.push('<li>' + $(this).html() + '</li>');
        });
        band_pass_filter_values.push('</ul>');
        fill_in_summary('sed', 'band_pass_filters', band_pass_filter_values);
    }

    var update_output_options = function() {
        var data_set_id = $(lc_id('galaxy_model')).find(':selected').attr('value');
        var $to = $(lc_id('output_properties'));
        var $from = $(lc_id('output_properties_from'));
        $to.find('option').each(function(i) {
            $(this).attr("selected", "selected");
        });
        var current = $to.val(); // in string format
        $to.empty();
        $from.empty();
        $.ajax({
            url : TAO_JSON_CTX + 'output_choices/' + data_set_id,
            dataType: "json",
            error: function() {
                alert("Couldn't get output choices");
            },
            success: function(data, status, xhr) {
                lc_output_props_widget.cache_store(data);
                lc_output_props_widget.display_selected(current, true);
            }
        });
    }

    var fill_in_summary = function(form_name, field_name, input_data) {
        $('div.summary_' + form_name + ' .' + field_name).html(input_data);
    }
    var clear_in_summary = function(form_name, field_name) {
        $('div.summary_' + form_name + ' .' + field_name).html('None');
    }

    var update_snapshot_options = function(){
        var simulation_id = $(lc_id('dark_matter_simulation')).val();
        var galaxy_model_id = $(lc_id('galaxy_model')).find(':selected').attr('data-galaxy_model_id');
        var $snapshot = $(lc_id('snapshot'));
        $snapshot.empty();
        var initial_snapshot = $snapshot.val();

        $.ajax({
            url : TAO_JSON_CTX + 'snapshots/' + simulation_id + ',' + galaxy_model_id,
            dataType: "json",
            error: function() {
                alert("Couldn't get snapshots");
            },
            success: function(data, status, xhr) {
                for(i=0; i<data.length; i++) {
                    var item = data[i];
                    $option = $('<option/>');
                    $option.attr('value',item.pk);
                    $option.html(item.fields.redshift);
                    if (item.pk == initial_snapshot) {
                        $option.attr('selected','selected');
                    }
                    $snapshot.append($option);
                }
                initial_snapshot = 0;
            }
        });
    };

    var update_filter_options = function(fetch_data, use_default){

        var data_set_id = $(lc_id('galaxy_model')).val();

        var isInt = function(value) {
            return !isNaN(parseInt(value)) && (parseFloat(value)+'' == parseInt(value)+'');
        }
        var isFloat = function(value) {
            return !isNaN(parseFloat(value));
        }

        function add_option($filter, item, current_filter) {
            $option = $('<option/>');
            $option.attr('value',item_to_value(item));
            if (item_to_value(item) == item_to_value(TAO_NO_FILTER)) {
                $option.html(item.fields.label);
            } else {
                if (item.fields.units != '') {
                    $option.html(item.fields.name + ' (' + item.fields.units + ')');
                } else {
                    $option.html(item.fields.name);
                }
            }
            if (item_to_value(item) == current_filter) {
                $option.attr('selected','selected');
            }
            $option.data('is_valid', item.fields.data_type==1? isFloat : isInt);
            $option.data('expected_type', item.fields.data_type==1? 'float' : 'integer');
            $filter.append($option);
        }

        function current_selection() {
            var list = [];
            $.each(lc_output_props_widget.selected(), function(i,value) {
               list.push('D-' + value);
            });
            $.each(sed_band_pass_filters_widget.selected(), function(i,value) {
                list.push('B-' + value);
            });
            return list;
        }

        function refresh_select(resp, use_default) {
            var $filter = $(rf_id('filter'));
            var current_filter = $filter.val();
            var current = current_selection();
            current.push(item_to_value(TAO_NO_FILTER));
            current.push('D-' + resp.default_id.toString());
            if (use_default || current.indexOf(current_filter) == -1) {
                current_filter = 'D-' + resp.default_id;
                if (current_filter == '' || current_filter == item_to_value(TAO_NO_FILTER)) {
                    $(rf_id('min')).val('');
                    $(rf_id('max')).val('');
                } else {
                    $(rf_id('min')).val(resp.default_min);
                    $(rf_id('max')).val(resp.default_max);
                }
            }
            $filter.empty();
            add_option($filter, TAO_NO_FILTER, current_filter);
            var data = resp.list;
            for(i=0; i<data.length; i++) {
                if (current.indexOf(item_to_value(data[i])) != -1) {
                    add_option($filter, data[i], current_filter);
                }
            }
            $filter.change();
        }

        if (!fetch_data && update_filter_options.current_data) {
            refresh_select(update_filter_options.current_data, use_default);
            return;
        }
        update_filter_options.current_data = undefined;
        $.ajax({
            url : TAO_JSON_CTX + 'filters/' + data_set_id,
            dataType: "json",
            error: function() {
                alert("Couldn't get filters");
            },
            success: function(resp, status, xhr) {
                update_filter_options.current_data = resp;
                refresh_select(resp, use_default);
            }
        });
    };

    var show_galaxy_model_info = function(galaxy_model_id) {
        var $galaxy_model_info = $('div.galaxy-model-info');
        if (galaxy_model_id === 0) {
            $galaxy_model_info.hide();
            return;
        }
        $.ajax({
            url : TAO_JSON_CTX + 'galaxy_model/' + galaxy_model_id,
            dataType: "json",
            error: function() {
                $galaxy_model_info.hide();
                alert("Couldn't get data for requested galaxy model");
            },
            success: function(data, status, xhr) {
                $('div.galaxy-model-info .name').html(data.fields.name);
                $('div.galaxy-model-info .details').html(data.fields.details);
                $galaxy_model_info.show();
                fill_in_summary('light_cone', 'galaxy_model', data.fields.name);
            }
        });
    };

    var update_galaxy_model_options = function(simulation_id){
        var $galaxy_model = $(lc_id('galaxy_model'));
        if (simulation_id === 0) {
            $galaxy_model.empty();
            $galaxy_model.change();
            return;
        }
        $.ajax({
            url : TAO_JSON_CTX + 'galaxy_models/' + simulation_id,
            dataType: "json",
            error: function() {
                $galaxy_model.empty();
                $galaxy_model.change();
                alert("Couldn't get data for requested simulation");
            },
            success: function(data, status, xhr) {
                var initial_data_set_id = $galaxy_model.val();
                $galaxy_model.empty();
                for(i=0; i<data.length; i++) {
                    item = data[i];
                    $option = $('<option/>');
                    $option.attr('value',item.id);
                    $option.attr('data-galaxy_model_id', item.galaxy_model_id);
                    if (item.id == initial_data_set_id) {
                        $option.attr('selected','selected');
                    }
                    $option.html(item.name);
                    $galaxy_model.append($option);
                }
                $galaxy_model.change();
            }
        });
    };

    var show_simulation_info = function(simulation_id) {
        $.ajax({
            url : TAO_JSON_CTX + 'simulation/' + simulation_id,
            dataType: "json",
            error: function() {
                $('div.simulation-info').hide();
                alert("Couldn't get data for requested simulation");
            },
            success: function(data, status, xhr) {
                $('div.simulation-info .name').html(data.fields.name);
                $('div.simulation-info .details').html(data.fields.details);
                $('div.simulation-info').show();
                fill_in_summary('light_cone', 'simulation', data.fields.name);
            }
        });
    };

    var show_dust_model_info = function(dust_id) {
        $.ajax({
            url : TAO_JSON_CTX + 'dust_model/' + dust_id,
            dataType: "json",
            error: function(){
                $('div.dust-model-info').hide();
                alert("Couldn't get data for requested dust model");
            },
            success: function(data, status, xhr) {
                $('div.dust-model-info .name').html(data.fields.name);
                $('div.dust-model-info .details').html(data.fields.details);
                $('div.dust-model-info').show();
                fill_in_summary('sed', 'dust_model', data.fields.name);
            }
        });
    };

    var clear_dust_model_info = function() {
        $('div.dust-model-info .name').html('');
        $('div.dust-model-info .details').html('');
        $('div.dust-model-info').show();
        clear_in_summary('sed', 'dust_model');
    }

    //
    // - event handlers for fields -
    //

    lc_output_props_widget.change_event(function(evt){
        update_filter_options(false, false);
        var output_properties_values = [];
        output_properties_values.push('<ul');
        $(lc_id('output_properties')+' option').each(function(i) {
            output_properties_values.push('<li>' + $(this).html() + '</li>');
        });
        output_properties_values.push('</ul');
        fill_in_summary('light_cone', 'output_properties', output_properties_values);
    });

    sed_band_pass_filters_widget.change_event(function(evt){
        update_filter_options(false, false);
        display_band_pass_filters_summary();
    });

    $(lc_id('dark_matter_simulation')).change(function(evt){
        var $this = $(this);
        var sim_id = $this.val();
        show_simulation_info(sim_id);
        update_galaxy_model_options(sim_id); // triggers galaxy_model.change
    });

    $(sed_id('select_dust_model')).change(function(evt){
        var $this = $(this);
        var dust_id = $this.val();
        show_dust_model_info(dust_id);
    });

    var bound = $('#RF_BOUND').val() == 'True';

    $(lc_id('galaxy_model')).change(function(evt){
        var $this = $(this);
        var galaxy_model_id = $this.find(':selected').attr('data-galaxy_model_id');
        show_galaxy_model_info(galaxy_model_id);
        var use_default = !update_filter_options.initializing || !bound;
        update_filter_options(true, use_default); // triggers filter.change
        update_filter_options.initializing = false;
        update_output_options();
        update_snapshot_options();
    });

    $(rf_id('filter')).change(function(evt){
        var $this = $(this);
        var filter_value = $this.val();

        if (filter_value == item_to_value(TAO_NO_FILTER)) {
            $(rf_id('max')).attr('disabled', 'disabled');
            $(rf_id('min')).attr('disabled', 'disabled')
            fill_in_summary('record_filter', 'record_filter', 'No Filter');
        } else {
            $(rf_id('max')).removeAttr('disabled');
            $(rf_id('min')).removeAttr('disabled');
            var filter_min = $(rf_id('min')).val();
            var filter_max = $(rf_id('max')).val();
            var filter_selected = $this.find('option:selected').html();
            if (!filter_min && !filter_max)
                fill_in_summary('record_filter', 'record_filter', filter_selected)
            else if (!filter_min)
                fill_in_summary('record_filter', 'record_filter', filter_selected + ' &lt; ' + filter_max);
            else if (!filter_max)
                fill_in_summary('record_filter', 'record_filter', filter_min + ' &lt; ' + filter_selected);
            else
                fill_in_summary('record_filter', 'record_filter', filter_min + ' &lt; ' + filter_selected + ' &lt; ' + filter_max);
        }
    });

    $(rf_id('min')).change(function(evt){
        var $this = $(this);
        var filter_min = $this.val();
        var filter_max = $(rf_id('max')).val();
        var filter_selected = $(rf_id('filter')).find('option:selected').html();
        if (!filter_max)
            fill_in_summary('record_filter', 'record_filter', filter_min + ' &lt; ' + filter_selected);
        else
            fill_in_summary('record_filter', 'record_filter', filter_min + ' &lt; ' + filter_selected + ' &lt; ' + filter_max);
    });

    $(rf_id('max')).change(function(evt){
        var $this = $(this);
        var filter_max = $this.val();
        var filter_min = $(rf_id('min')).val();
        var filter_selected = $(rf_id('filter')).find('option:selected').html();
        if (!filter_min)
            fill_in_summary('record_filter', 'record_filter', filter_selected + ' &lt; ' + filter_max);
        else
            fill_in_summary('record_filter', 'record_filter', filter_min + ' &lt; ' + filter_selected + ' &lt; ' + filter_max);
    });


    $(sed_id('band_pass_filters_add_link')).change(function() {
        fill_in_summary('sed', 'band_pass_filters', 'band_pass_filters_add_link.click()');
        $(sed_id('band_pass_filters_to')).change();
    });
    $(sed_id('band_pass_filters_remove_link')).click(function() {
        $(sed_id('band_pass_filters_to')).change();
    });
    $(sed_id('band_pass_filters_add_all_link')).click(function(evt) {
        fill_in_summary('sed', 'band_pass_filters', 'band_pass_filters_add_all_link.click()');
        $(sed_id('band_pass_filters_to')).change();
    });
    $(sed_id('band_pass_filters_remove_all_link')).click(function() {
        $(sed_id('band_pass_filters_to')).change();
    });

    $(lc_id('catalogue_geometry')).change(function(evt){
        var $this = $(this);
        var catalogue_geometry_value = $this.val();

        var light_cone_fields = $('.light_cone_field').closest('div.control-group');
        var light_box_fields = $('.light_box_field').closest('div.control-group');

        if (catalogue_geometry_value == "box") {
            light_box_fields.show();
            light_cone_fields.hide();
            fill_in_summary('light_cone', 'geometry_type', 'Box');
            $('div.summary_light_cone .box_fields').show();
            $('div.summary_light_cone .light_cone_fields').hide();
            $(lc_id('snapshot')).change();
        } else {
            light_box_fields.hide();
            light_cone_fields.show();
            fill_in_summary('light_cone', 'geometry_type', 'Light-Cone');
            $('div.summary_light_cone .box_fields').hide();
            $('div.summary_light_cone .light_cone_fields').show();
        }
    });

    function init_output_properties() {
        var current = [];
        var pseudo_json = [];
        $(lc_id('output_properties') + ' option').each(function(){
            var $this = $(this);
            var item = {pk: $this.attr('value'), fields:{name: $this.text()}};
            pseudo_json.push(item);
            if($this.attr('selected')) {
               current.push(item.pk);
            }
        });
        lc_output_props_widget.cache_store(pseudo_json);
        return current;
    }

    function init_bandpass_properties() {
        var current = [];
        var pseudo_json = [];
        $(sed_id('band_pass_filters') + ' option').each(function(){
            var $this = $(this);
            var item = {pk: $this.attr('value'), fields:{name: $this.text()}};
            pseudo_json.push(item);
            if($this.attr('selected')) {
                current.push(item.pk);
            }
        });
        sed_band_pass_filters_widget.cache_store(pseudo_json);
        return current;
    }


    $(lc_id('ra_opening_angle')).change(function(evt){
        var $this = $(this);
        var ra_opening_angle_value = $this.val();
        fill_in_summary('light_cone', 'ra_opening_angle', ra_opening_angle_value);
    });

    $(lc_id('dec_opening_angle')).change(function(evt){
        var $this = $(this);
        var dec_opening_angle_value = $this.val();
        fill_in_summary('light_cone', 'dec_opening_angle', dec_opening_angle_value);
    });

    $(lc_id('redshift_min')).change(function(evt){
        var $this = $(this);
        var redshift_min_value = $this.val();
        fill_in_summary('light_cone', 'redshift_min', redshift_min_value);
    });

    $(lc_id('redshift_max')).change(function(evt){
        var $this = $(this);
        var redshift_max_value = $this.val();
        fill_in_summary('light_cone', 'redshift_max', redshift_max_value);
    });

    $(lc_id('light_cone_type_0')+', '+lc_id('light_cone_type_1')).click(function(evt){
        var $this = $(this);
        fill_in_summary('light_cone', 'light_cone_type', $this.attr('value'));
    });

    $(lc_id('box_size')).change(function(evt){
        var $this = $(this);
        var box_size_value = $this.val();
        fill_in_summary('light_cone', 'box_size', box_size_value);
    });

    $(lc_id('snapshot')).change(function(evt){
        var $this = $(this);
        var snapshot_value = $this.find('option:selected').html();
        fill_in_summary('light_cone', 'snapshot', snapshot_value);
    });


    $(sed_id('single_stellar_population_model')).change(function(evt){
        var $this = $(this);
        var single_stellar_population_model_value = $this.find('option:selected').html();
        fill_in_summary('sed', 'single_stellar_population_model', single_stellar_population_model_value);
    });

    $(sed_id('apply_dust')).change(function(evt){
        if ($(sed_id('apply_dust')).is(':checked')) {
            $(sed_id('select_dust_model')).removeAttr('disabled');
            $(sed_id('select_dust_model')).change();
        }
        else {
            $(sed_id('select_dust_model')).attr('disabled', 'disabled');
            clear_dust_model_info();
        }
    });

    $(sed_id('apply_sed')).change(function(evt){
        if ($(sed_id('apply_sed')).is(':checked')) {
            $('#tao-tabs-2').css({"border-style": "solid"});
            $('#tao-tabs-2').css({"color": "#2BA6CB"});
            $(sed_id('single_stellar_population_model')).removeAttr('disabled');
            $(sed_id('single_stellar_population_model')).change();
            $(sed_id('band_pass_filters_filter')).removeAttr('disabled');
            $(sed_id('band_pass_filters_from')).removeAttr('disabled');
            sed_band_pass_filters_widget.set_enabled(true);
            $(sed_id('band_pass_filters')).removeAttr('disabled');
            display_band_pass_filters_summary();
            $(sed_id('apply_dust')).removeAttr('disabled');
            $(sed_id('apply_dust')).change();
        }
        else {
            $('#tao-tabs-2').css({"border-style": "dashed"});
            $('#tao-tabs-2').css({"color": "rgb(119, 221, 252)"});
            $(sed_id('single_stellar_population_model')).attr('disabled', 'disabled');
            clear_in_summary('sed', 'single_stellar_population_model');
            $(sed_id('band_pass_filters_filter')).attr('disabled', 'disabled');
            $(sed_id('band_pass_filters_from')).attr('disabled', 'disabled');
            sed_band_pass_filters_widget.set_enabled(false);
            $(sed_id('band_pass_filters')).attr('disabled', 'disabled');
            clear_in_summary('sed', 'band_pass_filters');
            $(sed_id('apply_dust')).attr('disabled', 'disabled');
            $(sed_id('select_dust_model')).attr('disabled', 'disabled');
            clear_dust_model_info();
        }
    });

    $('#id_output_format-supported_formats').change(function(evt){
        var $this = $(this);
        var output_format_value = $this.val();
        fill_in_summary('output', 'output_format', output_format_value);
    });

    var validate_min_max = function() {

        var min = $(rf_id('min')).val();
        var max = $(rf_id('max')).val();
        var $filter = $(rf_id('filter'));
        if ($filter.val() == item_to_value(TAO_NO_FILTER)) { return true; }
        var $option = $filter.find('option:selected');
        var is_valid = $option.data('is_valid');
        var expected_type = $option.data('expected_type');
        var error = false;
        if (min && !is_valid(min)) {
            show_error($(rf_id('min')),'Min in record filter should be ' + expected_type);
            error = true;
        } else {
            show_error($(rf_id('min')), null);
        }
        if (max && !is_valid(max)) {
            show_error($(rf_id('max')),'Max in record filter should be ' + expected_type);
            error = true;
        } else {
            show_error($(rf_id('max')), null);
        }

        return !error;
    }

    var cleanup_fields = function($form) {
        // cleanup geometry
        var geometry = $(lc_id('catalogue_geometry')).val();
        if (geometry == "box") {
            $('.light_cone_field').val('');
        } else {
            $('.light_box_field').val('');
        }
        // cleanup record filter
        var filter = $(rf_id('filter')).val();
        if (filter == item_to_value(TAO_NO_FILTER)) {
            $(rf_id('min')).val('');
            $(rf_id('max')).val('');
        }
    }

    //
    // -- form handler
    //
    $('#mgf-form').submit(function(){
        var $form = $(this);
        cleanup_fields($form);
        if (!validate_min_max()) { return false; }
        $(lc_id('output_properties')+' option').each(function(i) {
            $(this).attr("selected", "selected");
        });
        $(sed_id('band_pass_filters')+' option').each(function(i) {
            $(this).attr("selected", "selected");
        });
    });

    function init_wizard() {
        function set_click(selector, direction) {
            $(selector).click(function(evt) {
                var $this = $(this);
                show_tab($this, direction);
            })
        }
        set_click('.tao-prev', -1);
        set_click('.tao-next', +1);
        $("#tabs").tabs().addClass("ui-tabs-vertical ui-helper-clearfix");
        $("#tabs li").removeClass("ui-corner-top").addClass("ui-corner-left");
        // pre-select error
        var $errors = $('div.control-group').filter('.error');
        if ($errors.length > 0) {
            show_tab($errors.first(),0);
        }
    }

    //
    // -- initialization, note that there is a chain of events triggered
    //    by dark_matter_simulation
    //
    (function(){
        var current_output = init_output_properties();
        var current_bandpass = init_bandpass_properties();
        lc_output_props_widget.display_selected(current_output, false);
        sed_band_pass_filters_widget.display_selected(current_bandpass, false);
        lc_output_props_widget.change();
        sed_band_pass_filters_widget.change();
        init_wizard();
        var init_light_cone_type_value = $('input[name="light_cone-light_cone_type"][checked="checked"]').attr('value');
        fill_in_summary('light_cone', 'light_cone_type', init_light_cone_type_value);
        update_filter_options.initializing = true;
        $(lc_id('dark_matter_simulation')).change();
        $(lc_id('catalogue_geometry')).change();
        $('#id_sed-single_stellar_population_model').change();
        $('#id_output_format-supported_formats').change();
        $(sed_id('apply_sed')).change();
        $(sed_id('apply_dust')).change();
    })();
});
