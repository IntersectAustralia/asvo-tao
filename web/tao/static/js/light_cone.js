jQuery(document).ready(function($) {

    var lc_id = function(bare_name) {
        return '#id_light_cone-' + bare_name;
    };

    var sed_id = function(bare_name) {
        return '#id_sed-' + bare_name;
    };

    var mi_id = function(bare_name) {
        return '#id_mock_image-' + bare_name;
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

    var display_maximum_number_light_cones = function($field, msg) {
        var $enclosing = $field.closest('label.control-label');
        $enclosing.find('span.lc_number-inline').remove();
        if (msg == null) return;
        $field.after('<span class="lc_number-inline"></span>');
        $enclosing.find('span.lc_number-inline').text(msg);
        show_tab($enclosing, 0);
    }

    var lc_output_props_widget = new TwoSidedSelectWidget(lc_id('output_properties'), true);

    var sed_band_pass_filters_widget = new TwoSidedSelectWidget(sed_id('band_pass_filters'), false);

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

    var format_redshift = function(redshift_string) {
        var redshift = parseFloat(redshift_string);
        var whole_digit = parseInt(redshift).toString().length;
        return redshift.toFixed(Math.max(5-whole_digit, 0));
    };

    var update_snapshot_options = function(){
        var simulation_id = $(lc_id('dark_matter_simulation')).val();
        var galaxy_model_id = $(lc_id('galaxy_model')).find(':selected').attr('data-galaxy_model_id');
        var $snapshot = $(lc_id('snapshot'));
        var current = $snapshot.val();
        $snapshot.empty();

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
                    // Redshift Formatting:
                    // The age of the universe as a function of redshift is 1 / (1 + z) where z is the redshift.
                    // So z=0 is the present, and z=Infinity is the Big Bang.
                    // This is a non-linear relationship with more variation at smaller z values.
                    // To present figures that are easy to read and have sensible precision, redshift will be displayed with up to 5 decimals.
                    $option.html(format_redshift(item.fields.redshift));
                    if (item.pk == current) {
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
                    $option.html(item.fields.label + ' (' + item.fields.units + ')');
                } else {
                    $option.html(item.fields.label);
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
            if ($(sed_id('apply_sed')).is(':checked')) {
                $.each(sed_band_pass_filters_widget.selected(), function(i,value) {
                    list.push('B-' + value);
                });
            }
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
                fill_in_summary('light_cone', 'galaxy_model_description', '<br><b>' + data.fields.name + ':</b><br>' + data.fields.details);
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
                fill_in_summary('light_cone', 'simulation_description', '<br><b>' + data.fields.name + ':</b><br>' + data.fields.details);
                $(lc_id('number_of_light_cones')).data("simulation-box-size", data.fields.box_size);
            }
        });
    };

    var show_stellar_model_info = function(stellar_id) {
        $.ajax({
            url : TAO_JSON_CTX + 'stellar_model/' + stellar_id,
            dataType: "json",
            error: function(){
                $('div.stellar-model-info').hide();
                alert("Couldn't get data for requested dust model");
            },
            success: function(data, status, xhr) {
                $('div.stellar-model-info .name').html(data.fields.name);
                $('div.stellar-model-info .details').html(data.fields.description);
                $('div.stellar-model-info').show();
                fill_in_summary('sed', 'stellar_model_description', '<br>' + data.fields.description);
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
                fill_in_summary('sed', 'dust_model_description', '<br>' + data.fields.details);
            }
        });
    };

    var show_output_property_info = function(cache_item) {
        $('div.output-property-info .name').html(cache_item.text);
        $('div.output-property-info .details').html(cache_item.description);
        $('div.output-property-info').show();
    }

    var clear_info = function(form_name, name) {
        $('div.' + name + '-info .name').html('');
        $('div.' + name + '-info .details').html('');
        $('div.' + name + '-info').show();
    }

    var show_bandpass_filter_info = function(cache_item) {
        $('div.band-pass-info .name').html(cache_item.text);
        $('div.band-pass-info .details').html(cache_item.description);
        $('div.band-pass-info').show();
    }
    //
    // - event handlers for fields -
    //

    $('#expand_dataset').click(function(e) {
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

    $('#expand_stellar_model').click(function(e) {
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

    $('#expand_dust_model').click(function(e) {
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

    var list_multiple_selections_in_summary = function(form_name, select_widget){
        console.log("list_multiple_selections_in_summary for " + select_widget + " starts")
        var selections_count = 0;
        var selected_values = [];

        selected_values.push('<ul>');
        var $groups = $('#id_' + form_name + '-' + select_widget +' optgroup');
        console.log(form_name + ' ' + select_widget + ' has group size: ' + $groups.size());
        if ($groups.size() > 0) {
            $groups.each(function(i, e) {
                var name = $(e).attr('group-name');
                if (name.length == 0) {
                    name = "Ungrouped";
                }
                selected_values.push('<li>' + name + '<ul>');
                $(e).find('option').each(function(i,option) {
                    selected_values.push('<li>' + $(option).html() + '</li>');
                    selections_count++;
                })
                selected_values.push('</ul></li>');
            })
        } else {
            $('#id_' + form_name + '-' + select_widget +' option').each(function(i,option) {
                selected_values.push('<li>' + $(option).html() + '</li>');
                selections_count++;
            });
        }
        selected_values.push('</ul>');

        fill_in_summary(form_name, select_widget + '_list', selected_values.join(''));
        console.log("list_multiple_selections_in_summary  " + select_widget + " ends")
        return selections_count;
    }

    lc_output_props_widget.change_event(function(evt){
        update_filter_options(false, false);
        var output_properties_count = list_multiple_selections_in_summary('light_cone', 'output_properties');

        if (output_properties_count == 1)
            fill_in_summary('light_cone', 'output_properties', output_properties_count + " property selected");
        else
            fill_in_summary('light_cone', 'output_properties', output_properties_count + " properties selected");
    });

    $('#expand_output_properties').click(function(e) {
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

    lc_output_props_widget.option_clicked_event(function(cache_item){
        show_output_property_info(cache_item);
    });

    var display_band_pass_filters_summary = function() {
        var band_pass_filter_count = list_multiple_selections_in_summary('sed', 'band_pass_filters');

        if (band_pass_filter_count == 1)
            fill_in_summary('sed', 'band_pass_filters', band_pass_filter_count + " filter selected");
        else
            fill_in_summary('sed', 'band_pass_filters', band_pass_filter_count + " filters selected");
    }

    sed_band_pass_filters_widget.change_event(function(evt){
        update_filter_options(false, false);
        display_band_pass_filters_summary();
    });

    $('#expand_band_pass_filters').click(function(e) {
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

    sed_band_pass_filters_widget.option_clicked_event(function(cache_item){
        show_bandpass_filter_info(cache_item);
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
        if (use_default) {
            var catalogue_geometry_value = $(lc_id('catalogue_geometry')).val();
            if (catalogue_geometry_value == "box") {
                var simulation_box_size = $(lc_id('number_of_light_cones')).data("simulation-box-size");
                $(lc_id('box_size')).val(simulation_box_size);
                $(lc_id('box_size')).change();
            }
        }
        update_filter_options(true, use_default); // triggers filter.change
        update_filter_options.initializing = false;
        update_output_options();
        update_snapshot_options();
    });

    var fill_in_selection_in_summary = function() {
        var filter_min = $(rf_id('min')).val();
        var filter_max = $(rf_id('max')).val();
        var filter_selected = $(rf_id('filter')).find('option:selected').html();
        if (!filter_min && !filter_max)
            fill_in_summary('record_filter', 'record_filter', filter_selected);
        else if (!filter_min)
            fill_in_summary('record_filter', 'record_filter', filter_selected + ' &le; ' + filter_max);
        else if (!filter_max)
            fill_in_summary('record_filter', 'record_filter', filter_min + ' &le; ' + filter_selected);
        else
            fill_in_summary('record_filter', 'record_filter', filter_min + ' &le; ' + filter_selected + ' &le; ' + filter_max);
    }

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
            fill_in_selection_in_summary();
        }
    });

    $(rf_id('min') + ', ' + rf_id('max')).change(function(evt){
        fill_in_selection_in_summary();
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
            console.log($this);
            var item = {pk: $this.attr('value'), fields:{label: $this.text()}};
            pseudo_json.push(item);
            if($this.attr('selected')) {
               current.push(item.pk);
            }
        });
        lc_output_props_widget.cache_store(pseudo_json);
        console.log('Current output properties: ' + current);
        return current;
    }

    function init_bandpass_properties() {
        var current = [];
        $(sed_id('band_pass_filters') + ' option').each(function(){
            var $this = $(this);
            if ($this.attr('selected')) {
                current.push($this.attr('value'));
            }
        });
        $.ajax({
            url : TAO_JSON_CTX + 'bandpass_filters/',
            dataType: "json",
            error: function(jqXHR, status, error) {
                alert("Couldn't get bandpass filters");
            },
            success: function(data, status, xhr) {
                sed_band_pass_filters_widget.cache_store(data);
                sed_band_pass_filters_widget.display_selected(current, false);
            }
        });
        console.log('Current bandpass filters: ' + current);
        return current;
    }

    var fill_in_ra_dec_in_summary = function() {
        var ra_opening_angle_value = $(lc_id('ra_opening_angle')).val();
        var dec_opening_angle_value = $(lc_id('dec_opening_angle')).val();
        if (!ra_opening_angle_value && !dec_opening_angle_value) {
            fill_in_summary('light_cone', 'ra_opening_angle', '');
            fill_in_summary('light_cone', 'dec_opening_angle', '');
        } else if (!ra_opening_angle_value) {
            fill_in_summary('light_cone', 'ra_opening_angle', '');
            fill_in_summary('light_cone', 'dec_opening_angle', 'Dec: ' + dec_opening_angle_value + '&deg;<br>');
        } else if (!dec_opening_angle_value) {
            fill_in_summary('light_cone', 'ra_opening_angle', 'RA: ' + ra_opening_angle_value + '&deg; <br>');
            fill_in_summary('light_cone', 'dec_opening_angle', '');
        } else {
            fill_in_summary('light_cone', 'ra_opening_angle', 'RA: ' + ra_opening_angle_value + '&deg;, ');
            fill_in_summary('light_cone', 'dec_opening_angle', 'Dec: ' + dec_opening_angle_value + '&deg;<br>');
        }
    }

    $(lc_id('ra_opening_angle') + ', ' + lc_id('dec_opening_angle')).change(function(evt){
        fill_in_ra_dec_in_summary();
        calculate_max_number_of_cones();
    });

    var fill_in_redshift_in_summary = function() {
        var redshift_max_value = $(lc_id('redshift_max')).val();
        var redshift_min_value = $(lc_id('redshift_min')).val();
        if (!redshift_min_value && !redshift_max_value) {
            fill_in_summary('light_cone', 'redshift_min', '')
            fill_in_summary('light_cone', 'redshift_max', '')
        }
        else if (!redshift_min_value) {
            fill_in_summary('light_cone', 'redshift_min', '')
            fill_in_summary('light_cone', 'redshift_max', 'Redshift: r &le; ' + redshift_max_value);
        }
        else if (!redshift_max_value) {
            fill_in_summary('light_cone', 'redshift_min', 'Redshift: ' + redshift_min_value + ' &le; r');
            fill_in_summary('light_cone', 'redshift_max', '')
        }
        else {
            fill_in_summary('light_cone', 'redshift_min', 'Redshift: ' + redshift_min_value + ' &le; r &le; ');
            fill_in_summary('light_cone', 'redshift_max', redshift_max_value);
        }
    }

    $(lc_id('redshift_min') + ', ' + lc_id('redshift_max')).change(function(evt){
        fill_in_redshift_in_summary();
        calculate_max_number_of_cones();
    });

    // Max's algorithm for calculating the maximum allowed number of unique light-cones
//    /**
//     * Convert redshift to distance
//     * @param z redshift
//     * @return comoving distance
//     */
    var redshift_to_distance = function(z) {
        var n = 1000;

        var c = 299792.458;
        var H0 = 100.0;
        var h = H0/100;
        var WM = 0.25;
        var WV = 1.0 - WM - 0.4165/(H0*H0);
        var WR = 4.165E-5/(h*h);
        var WK = 1-WM-WR-WV;
        var az = 1.0/(1+1.0*z);
        var DTT = 0.0;
        var DCMR = 0.0;
        for (var i = 0; i < n; i++) {
            var a = az+(1-az)*(i+0.5)/n;
            var adot = Math.sqrt(WK+(WM/a)+(WR/(a*a))+(WV*a*a));
            DTT = DTT + 1.0/adot;
            DCMR = DCMR + 1.0/(a*adot);
        }
        DTT = (1.-az)*DTT/n;
        DCMR = (1.-az)*DCMR/n;
        var d = (c/H0)*DCMR;

        return d;
    }
//    /**
//     * Compute the maximum number of unique cones available for selected parameters
//     */
     var get_number_of_unique_light_cones = function() {
        var alfa1 = parseFloat($(lc_id('ra_opening_angle')).val());
        var box_side = $(lc_id('number_of_light_cones')).data("simulation-box-size");
        var d1 = redshift_to_distance(parseFloat($(lc_id('redshift_min')).val()));
        var d2 = redshift_to_distance(parseFloat($(lc_id('redshift_max')).val()));
        var beta1;
        for (beta1 = alfa1; beta1 < 90; beta1 = beta1 + 0.01) {
            if ((d2 - box_side)*Math.sin((Math.PI/180)*(beta1+alfa1)) <= d2*Math.sin((Math.PI/180)*beta1)) {
                break;
            }
        }
        var hv = Math.floor(d2*Math.sin((Math.PI/180)*(alfa1+beta1)) - d1*Math.sin((Math.PI/180)*(alfa1+beta1)));

        var hh = 2*d2*Math.sin((Math.PI/180)*(parseFloat($(lc_id('dec_opening_angle')).val()))/2);

        var nv = Math.floor(box_side/hv);
        var nh = Math.floor(box_side/hh);
        var n = nv*nh;

        return n;
    }

    var spinner_check_value = function(new_value) {
        var maximum = $(lc_id('number_of_light_cones')).data('spin-max');
        var $spinner = $(lc_id('number_of_light_cones')).closest('span');
        if (maximum <= 0) {
            show_error($spinner, "Selection parameters can't be used to generate unique light-cones");
            fill_in_summary('light_cone', 'number_of_light_cones', 'An invalid number of light cones is selected');
            return false;
        }
        else {
            if (new_value <= 0) {
                show_error($spinner, "Please provide a positive number of light-cones");
                fill_in_summary('light_cone', 'number_of_light_cones', 'Negative number of light cones is invalid');
                $('.ui-spinner-down').button('disable').addClass("ui-state-disabled").removeClass('ui-state-enabled');
                return false;
            }
            else if (new_value > maximum) {
                show_error($spinner, "The maximum is " + maximum);
                fill_in_summary('light_cone', 'number_of_light_cones', 'Number of light cones selected exceeds the maximum');
                $('.ui-spinner-up').button('disable').addClass("ui-state-disabled").removeClass('ui-state-enabled');
                return false;
            }
        }
        $('.ui-spinner-down').button('enable').addClass('ui-state-enabled').removeClass("ui-state-disabled");
        $('.ui-spinner-up').button('enable').addClass('ui-state-enabled').removeClass("ui-state-disabled");
        show_error($spinner, null);
        fill_in_summary('light_cone', 'number_of_light_cones', new_value +  " " + $("input[name='light_cone-light_cone_type']:checked").val() + " light cones");
        return true;
    }

    var calculate_max_number_of_cones = function() {
        function spinner_set_max(maximum) {
            $spinner_label = $('label[for=id_light_cone-number_of_light_cones]');
            if ( isNaN(maximum) || maximum <= 0 || !isFinite(maximum)){
                $(lc_id('number_of_light_cones')).spinner("disable");
                $(lc_id('number_of_light_cones')).data("spin-max", 0);
                $spinner_label.html("Select the number of light-cones:*");
            }
            else {
                $(lc_id('number_of_light_cones')).spinner("enable");
                $(lc_id('number_of_light_cones')).data("spin-max",maximum);
                $spinner_label.html("Select the number of light-cones: (maximum for the selected parameters is " + maximum + ")*");
            }
            spinner_check_value(parseInt($(lc_id('number_of_light_cones')).val()));
        }

        var selection = $("input[name='light_cone-light_cone_type']:checked").val();
        if ("unique" == selection) {
            var maximum = get_number_of_unique_light_cones();
            spinner_set_max(maximum);
        } else {
            $.ajax({
                url : TAO_JSON_CTX + 'global_parameter/' + 'maximum-random-light-cones',
                dataType: "json",
                error: function() {
                    alert("Couldn't get data for maximum-random-light-cones");
                },
                success: function(data, status, xhr) {
                    var maximum = parseInt(data.fields.parameter_value);
                    spinner_set_max(maximum);
                    display_maximum_number_light_cones($(lc_id('number_of_light_cones')), maximum);
                }
            });
        }
    }

    $(lc_id('light_cone_type_0')+', '+lc_id('light_cone_type_1')).click(function(evt){
        var $this = $(this);
        fill_in_summary('light_cone', 'light_cone_type', $this.attr('value'));
        calculate_max_number_of_cones();
    });

    $(lc_id('number_of_light_cones')).spinner({
        spin: function(evt, ui) {
            return spinner_check_value(ui.value);
        }
    });

    $(lc_id('number_of_light_cones')).change(function() {
       var new_value = parseInt($(this).val());
       return spinner_check_value(new_value);
    });

    $(lc_id('box_size')).change(function(evt){
        var $this = $(this);
        var box_size_value = parseFloat($this.val());
        var max_box_size = parseFloat($(lc_id('number_of_light_cones')).data("simulation-box-size"));
        if (isNaN(box_size_value)) {
            show_error($(lc_id('box_size')),'Box size must be a number');
            return false;
        }
        if (!isNaN(max_box_size) && parseFloat(box_size_value) > parseFloat(max_box_size)) {
            show_error($(lc_id('box_size')),'Box size greater than simulation\'s box size');
            return false;
        }
        show_error($(lc_id('box_size')), null);
        fill_in_summary('light_cone', 'box_size', box_size_value);
    });

    $(lc_id('snapshot')).change(function(evt){
        var $this = $(this);
        var snapshot_value = $this.find('option:selected').html();
        fill_in_summary('light_cone', 'snapshot', snapshot_value);
    });


    $(sed_id('single_stellar_population_model')).change(function(evt){
        var $this = $(this);
        show_stellar_model_info($this.val())
        var single_stellar_population_model_value = $this.find('option:selected').html();
        fill_in_summary('sed', 'single_stellar_population_model', single_stellar_population_model_value);
    });

    $(sed_id('apply_dust')).change(function(evt){
        if ($(sed_id('apply_dust')).is(':checked')) {
            $(sed_id('select_dust_model')).removeAttr('disabled');
            $(sed_id('select_dust_model')).change();
            $('#expand_dust_model').show();
        }
        else {
            $(sed_id('select_dust_model')).attr('disabled', 'disabled');
            clear_info('sed', 'dust-model');
            clear_in_summary('sed', 'dust_model');
            $('#expand_dust_model').hide();
            $('div.summary_sed .dust_model_description').hide();
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
            $('div.summary_sed .apply_sed').show();
            fill_in_summary('sed', 'select_sed', '');
            display_band_pass_filters_summary();
            $(sed_id('apply_dust')).removeAttr('disabled');
            $(sed_id('apply_dust')).change();
            update_filter_options(false, false); // triggers filter.change
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
            clear_info('sed', 'stellar-model');
            clear_info('sed', 'band-pass');
            clear_info('sed', 'dust-model');
            $('div.summary_sed .apply_sed').hide();
            fill_in_summary('sed', 'select_sed', 'Not selected');
            var use_default = !update_filter_options.initializing || !bound;
            update_filter_options(false, use_default); // triggers filter.change
        }
        $('#sed_params').slideToggle();
        $('#sed_info').slideToggle();
    });

    $('#id_output_format-supported_formats').change(function(evt){
        var $this = $(this);
        var output_format_value = $this.find('option:selected').text();
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

    var validate_number_of_light_cones = function() {
        var geometry = $(lc_id('catalogue_geometry')).val();
        if (geometry == "light-cone") {
            var number_of_light_cones = parseInt($(lc_id('number_of_light_cones')).val());
            return spinner_check_value(number_of_light_cones);
        }
        return true;
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
        var min_max_valid = validate_min_max();
        var number_of_light_cones_valid = validate_number_of_light_cones();
        if (!min_max_valid || !number_of_light_cones_valid) {
            return false;
        }
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
        $("#tabs").tabs({
            beforeActivate: update_tabs
        }).addClass("ui-tabs-vertical ui-helper-clearfix");
        $("#tabs li").removeClass("ui-corner-top").addClass("ui-corner-left");
        // pre-select error
        var $errors = $('div.control-group').filter('.error');
        if ($errors.length > 0) {
            show_tab($errors.first(),0);
        }
    }

    function mock_image_enabled() {
        var ami = $('#id_mock_image-apply_mock_image');
        return ami.attr('disabled') === undefined && ami.is(':checked');
    }

    function update_apply_mock_image() {
        if(mock_image_enabled()) {
            $('#tao-tabs-3').css({"border-style": "solid"});
            $('#tao-tabs-3').css({"color": "#2BA6CB"});

            // Add an image if there is none there.
            if($('#mock_image_params .single-form').length == 0)
                $('#mock_image_params .add-row').click();

            $('#mock_image_params').slideDown();
            $('#mock_image_info').slideDown();
        }
        else {
            $('#tao-tabs-3').css({"border-style": "dashed"});
            $('#tao-tabs-3').css({"color": "rgb(119, 221, 252)"});
            $('#mock_image_params').slideUp();
            $('#mock_image_info').slideUp();
        }
        update_mock_image_summary();
    }

    function update_mock_image_magnitudes(sel) {
        if(sel === undefined)
            sel = $('#mock_image_params select[name$="mag_field"]');
        update_select(sel, $('#id_sed-band_pass_filters > option'));
    }

    $(mi_id('apply_mock_image')).change(function(evt){
        update_apply_mock_image();
    });

    function update_mock_image_sub_cones(sel) {
        if(sel === undefined)
            sel = $('#mock_image_params select[name$="sub_cone"]');
        var num_cones = parseInt($('#id_light_cone-number_of_light_cones').val());
        sel.each(function(){
            var cur = $(this).children('option:selected').attr('value');
            $(this).empty();
            $(this).append($('<option/>').attr('value', 'ALL').text('All'));
            if(num_cones !== undefined && num_cones > 1) {
                for(var ii=0; ii<num_cones; ii++) {
                    var opt = $('<option/>').attr('value', ii).text(ii);
                    if(opt.attr('value') == cur)
                        opt.prop('selected', true);
                    $(this).append(opt);
                }
            }
        });
    }

    function update_mock_image_summary() {
        if(mock_image_enabled()) {
            $('div.summary_mock_image .apply_mock_image').show();
            fill_in_summary('mock_image', 'select_mock_image', '');
            fill_in_summary('mock_image', 'num_images', $('#mock_image_params .single-form').length);
        }
        else {
            $('div.summary_mock_image .apply_mock_image').hide();
            fill_in_summary('mock_image', 'select_mock_image', 'Not selected');
        }
    }

    function update_select(sel, opts) {
        sel.each(function() {
            var cur_sel = $(this);
            var cur_opt = cur_sel.children('option:selected').attr('value');
            cur_sel.empty();
            opts.each(function(){
                var opt = $('<option/>').attr('value', $(this).attr('value')).text($(this).text());
                if($(this).attr('value') == cur_opt)
                    opt.prop('selected', true);
                cur_sel.append(opt);
            });
            cur_sel.change();
        });
    }

    function update_tabs(event, ui) {
        var old_tab = $(ui.oldTab).children('a:first').attr('id');
        var new_tab = $(ui.newTab).children('a:first').attr('id');

        // Check if the mock-image tab should be enabled.
        if(old_tab == 'tao-tabs-1' || old_tab == 'tao-tabs-2') {
            var sel = $('#id_light_cone-catalogue_geometry option:selected').val();
            if($('#id_light_cone-catalogue_geometry option:selected').val() == 'light-cone' &&
               $('#id_sed-apply_sed').is(':checked')) {
                $(mi_id('apply_mock_image')).removeAttr('disabled');
                update_apply_mock_image();
            }
            else {
                $(mi_id('apply_mock_image')).attr('disabled', 'disabled');
                update_apply_mock_image();
            }
        }

        // Update all mock image magnitudes.
        if(old_tab == 'tao-tabs-2')
            update_mock_image_magnitudes();

        // Update every mock image sub-cone option with appropriate
        // values from the general properties.
        if(old_tab == 'tao-tabs-1')
            update_mock_image_sub_cones();

        // Upon moving to a new tab, run validation in the tab to pick up
        // any changes from previous tab.
        if(new_tab == 'tao-tabs-3')
            $.validate_form('mock_image');
    }

    function mock_image_setup_form(form) {
        var ra = $('#id_light_cone-ra_opening_angle').val();
        var dec = $('#id_light_cone-dec_opening_angle').val();
        var z_min = $('#id_light_cone-redshift_min').val();
        var z_max = $('#id_light_cone-redshift_max').val();
        update_mock_image_sub_cones(form.find('select[name$="sub_cone"]'));
        update_mock_image_magnitudes(form.find('select[name$="mag_field"]'));
        form.find('input[name$="min_mag"]').val(7);
        form.find('input[name$="z_min"]').val(z_min);
        form.find('input[name$="z_max"]').val(z_max);
        if(ra != "") {
            form.find('input[name$="origin_ra"]').val(ra/2.0);
            form.find('input[name$="fov_ra"]').val(ra);
        }
        if(dec !== "") {
            form.find('input[name$="origin_dec"]').val(dec/2.0);
            form.find('input[name$="fov_dec"]').val(dec);
        }
        form.find('input[name$="width"]').val(1024);
        form.find('input[name$="height"]').val(1024);
        update_mock_image_summary();

        $('.delete-row:last').click(function(){
            update_mock_image_summary();
            return true;
        });

        //
        // Setup validation on each input.
        //

        // z_min
        form.find('input[name$="z_min"]').validate({
            type: 'float',
            cache: {
                z_min: [$('#id_light_cone-redshift_min'), 'float'],
                z_max: [$('#id_light_cone-redshift_max'), 'float']
            },
            group: [form.find('input[name$="z_max"]')],
            form: 'mock_image'
        }).validate('test', {
            check: function(val, cache) {
                return val >= cache.z_min;
            },
            message: ['Value must be greater than the minimum redshift of ',
                      'the cone specified in General Properties.'].join('')
        }).validate('test', {
            check: function(val, cache) {
                return val <= cache.z_max;
            },
            message: ['Value must be less than the maximum redshift of ',
                      'the cone specified in General Properties.'].join('')
        }).validate('test', {
            check: function(val, cache) {
                return val <= form.find('input[name$="z_max"]').val();
            },
            message: ['Value must be less than the maximum redshift of ',
                      'this mock image.'].join('')
        });

        // z_max
        form.find('input[name$="z_max"]').validate({
            type: 'float',
            cache: {
                z_min: [$('#id_light_cone-redshift_min'), 'float'],
                z_max: [$('#id_light_cone-redshift_max'), 'float']
            },
            group: [form.find('input[name$="z_min"]')],
            form: 'mock_image'
        }).validate('test', {
            check: function(val, cache) {
                return val <= cache.z_max;
            },
            message: ['Value must be less than the maximum redshift of ',
                      'the cone specified in General Properties.'].join('')
        }).validate('test', {
            check: function(val, cache) {
                return val >= cache.z_min;
            },
            message: ['Value must be greater than the minimum redshift of ',
                      'the cone specified in General Properties.'].join('')
        }).validate('test', {
            check: function(val, cache) {
                return val >= form.find('input[name$="z_min"]').val();
            },
            message: ['Value must be greater than the minimum redshift of ',
                      'this mock image.'].join('')
        });

        // origin_ra
        form.find('input[name$="origin_ra"]').validate({
            type: 'float',
            cache: {
                ra: [$('#id_light_cone-ra_opening_angle'), 'float'],
                fov_ra: [form.find('input[name$="fov_ra"]'), 'float']
            },
            group: [form.find('input[name$="fov_ra"]')],
            form: 'mock_image'
        }).validate('test', {
            check: function(val, cache) {
                return val + 0.5*cache.fov_ra <= cache.ra;
            },
            message: 'Origin and field-of-view RAs exceed cone maximum.'
        }).validate('test', {
            check: function(val, cache) {
                return val - 0.5*cache.fov_ra >= 0;
            },
            message: 'Origin and field-of-view RAs are below cone minimum.'
        });

        // origin_dec
        form.find('input[name$="origin_dec"]').validate({
            type: 'float',
            cache: {
                dec: [$('#id_light_cone-dec_opening_angle'), 'float'],
                fov_dec: [form.find('input[name$="fov_dec"]'), 'float']
            },
            group: [form.find('input[name$="fov_dec"]')],
            form: 'mock_image'
        }).validate('test', {
            check: function(val, cache) {
                return val + 0.5*cache.fov_dec <= cache.dec;
            },
            message: 'Origin and field-of-view DECs exceed cone maximum.'
        }).validate('test', {
            check: function(val, cache) {
                return val - 0.5*cache.fov_dec >= 0;
            },
            message: 'Origin and field-of-view DECs are below cone minimum.'
        });

        // fov_ra
        form.find('input[name$="fov_ra"]').validate({
            type: 'float',
            cache: {
                ra: [$('#id_light_cone-ra_opening_angle'), 'float'],
                o_ra: [form.find('input[name$="origin_ra"]'), 'float']
            },
            group: [form.find('input[name$="origin_ra"]')],
            form: 'mock_image'
        }).validate('test', {
            check: function(val, cache) {
                return cache.o_ra + 0.5*val <= cache.ra;
            },
            message: 'Origin and field-of-view RAs exceed cone maximum.'
        }).validate('test', {
            check: function(val, cache) {
                return cache.o_ra - 0.5*val >= 0;
            },
            message: 'Origin and field-of-view RAs are below cone minimum.'
        });

        // fov_dec
        form.find('input[name$="fov_dec"]').validate({
            type: 'float',
            cache: {
                dec: [$('#id_light_cone-dec_opening_angle'), 'float'],
                o_dec: [form.find('input[name$="origin_dec"]'), 'float']
            },
            group: [form.find('input[name$="origin_dec"]')],
            form: 'mock_image'
        }).validate('test', {
            check: function(val, cache) {
                return cache.o_dec + 0.5*val <= cache.dec;
            },
            message: 'Origin and field-of-view DECs exceed cone maximum.'
        }).validate('test', {
            check: function(val, cache) {
                return cache.o_dec - 0.5*val >= 0;
            },
            message: 'Origin and field-of-view DECs are below cone minimum.'
        });

        // width
        form.find('input[name$="width"]').validate({
            type: 'int',
            form: 'mock_image'
        }).validate('test', {
            check: function(val) {
                return val > 1;
            },
            message: 'Image must have at least 1 pixel in width.'
        }).validate('test', {
            check: function(val) {
                return val < 4096;
            },
            message: 'Maximum image width is 4096 pixels.'
        });

        // height
        form.find('input[name$="height"]').validate({
            type: 'int',
            form: 'mock_image'
        }).validate('test', {
            check: function(val) {
                return val > 1;
            },
            message: 'Image must have at least 1 pixel in height.'
        }).validate('test', {
            check: function(val) {
                return val < 4096;
            },
            message: 'Maximum image height is 4096 pixels.'
        });
    }

    //
    // -- initialization, note that there is a chain of events triggered
    //    by dark_matter_simulation
    //
    (function(){
        var current_output = init_output_properties();
        var current_bandpass = init_bandpass_properties();
        lc_output_props_widget.display_selected(current_output, false);
//        sed_band_pass_filters_widget.display_selected(current_bandpass, false);
        lc_output_props_widget.change();
        sed_band_pass_filters_widget.change();
        init_wizard();
        var init_light_cone_type_value = $('input[name="light_cone-light_cone_type"][checked="checked"]').attr('value');
        fill_in_summary('light_cone', 'number_of_light_cones',  $(lc_id('number_of_light_cones')).val() +  " " + init_light_cone_type_value + " light cones");
        $(lc_id('number_of_light_cones')).attr('class', 'light_cone_field'); // needed to associate the spinner with light-cone only, not when selecting box
        update_filter_options.initializing = true;
        $(lc_id('dark_matter_simulation')).change();
        $(lc_id('catalogue_geometry')).change();
        $('#id_output_format-supported_formats').change();
        $(sed_id('apply_sed')).change();
        $(sed_id('apply_dust')).change();

        $('div.summary_light_cone .output_properties_list').hide();
        $('div.summary_sed .band_pass_filters_list').hide();
        $('div.summary_light_cone .simulation_description, div.summary_light_cone .galaxy_model_description').hide();
        $('div.summary_sed .stellar_model_description').hide();
        $('div.summary_sed .dust_model_description').hide();
        fill_in_ra_dec_in_summary();
        fill_in_redshift_in_summary();
        fill_in_summary('light_cone', 'box_size', $(lc_id('box_size')).val());
        fill_in_summary('light_cone', 'snapshot', format_redshift($(lc_id('snapshot')+' option:selected').html()));
        setTimeout(function(){
            display_band_pass_filters_summary();
        }, 1000);

        // Prepare the mock image formset.
        $('#mock_image_params .single-form').formset({
            prefix: 'mock_image'
        });

        // We always have an extra form at the end, so delete it
        // now that we've initialised the formset.
        $('#mock_image_params .single-form:last').remove();

        // Pretty up the "add another" button and add my own click handler.
        $('.add-row').button().click(function(){
            mock_image_setup_form($('#mock_image_params .single-form:last'));
            return true;
        });
    })();
});
