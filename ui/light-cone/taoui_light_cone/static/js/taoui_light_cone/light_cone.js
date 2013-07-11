
var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};


catalogue.modules.light_cone = function($) {

  console.log('new light_cone modules');

  this.lc_output_props_widget = new TwoSidedSelectWidget(lc_id('output_properties'), true);

  function get_widget() {
    return catalogue.modules.light_cone.lc_output_props_widget;
  }

  var display_maximum_number_light_cones = function($field, msg) {
        var $enclosing = $field.closest('label.control-label');
        $enclosing.find('span.lc_number-inline').remove();
        if (msg == null) return;
        $field.after('<span class="lc_number-inline"></span>');
        $enclosing.find('span.lc_number-inline').text(msg);
        show_tab($enclosing, 0);
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
                get_widget().cache_store(data);
                update_filter_options.output_props = true;
                get_widget().display_selected(current, true);
            }
        });
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
        get_widget().cache_store(pseudo_json);
        console.log('Current output properties: ' + current);
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

    // $(lc_id('ra_opening_angle') + ', ' + lc_id('dec_opening_angle')).change(function(evt){
    //     fill_in_ra_dec_in_summary();
    //     calculate_max_number_of_cones();
    // });

    var fill_in_redshift_in_summary = function() {
        var redshift_max_value = $(lc_id('redshift_max')).val();
        var redshift_min_value = $(lc_id('redshift_min')).val();
        if (!redshift_min_value && !redshift_max_value) {
            fill_in_summary('light_cone', 'redshift_min', '')
            fill_in_summary('light_cone', 'redshift_max', '')
        }
        else if (!redshift_min_value) {
            fill_in_summary('light_cone', 'redshift_min', '')
            fill_in_summary('light_cone', 'redshift_max', 'Redshift: z &le; ' + redshift_max_value);
        }
        else if (!redshift_max_value) {
            fill_in_summary('light_cone', 'redshift_min', 'Redshift: ' + redshift_min_value + ' &le; z');
            fill_in_summary('light_cone', 'redshift_max', '')
        }
        else {
            fill_in_summary('light_cone', 'redshift_min', 'Redshift: ' + redshift_min_value + ' &le; z &le; ');
            fill_in_summary('light_cone', 'redshift_max', redshift_max_value);
        }
    }


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
        var ra = $(lc_id('ra_opening_angle')).val();
        var dec = $(lc_id('dec_opening_angle')).val();
        var redshift_min = $(lc_id('redshift_min')).val();
        var redshift_max = $(lc_id('redshift_max')).val();

        var alfa1 = parseFloat(ra);
        var box_side = $(lc_id('number_of_light_cones')).data("simulation-box-size");
        var d1 = redshift_to_distance(parseFloat(redshift_min));
        var d2 = redshift_to_distance(parseFloat(redshift_max));
        var beta1;
        for (beta1 = alfa1; beta1 < 90; beta1 = beta1 + 0.01) {
            if ((d2 - box_side)*Math.sin((Math.PI/180)*(beta1+alfa1)) <= d2*Math.sin((Math.PI/180)*beta1)) {
                break;
            }
        }
        var hv = Math.floor(d2*Math.sin((Math.PI/180)*(alfa1+beta1)) - d1*Math.sin((Math.PI/180)*(alfa1+beta1)));

        var hh = 2*d2*Math.sin((Math.PI/180)*(parseFloat(dec))/2);

        var nv = Math.floor(box_side/hv);
        var nh = Math.floor(box_side/hh);
        var n = nv*nh;

        return n;
    }

    var spinner_check_value = function(new_value) {
        var ra = $(lc_id('ra_opening_angle')).val();
        var dec = $(lc_id('dec_opening_angle')).val();
        var redshift_min = $(lc_id('redshift_min')).val();
        var redshift_max = $(lc_id('redshift_max')).val();
        var $spinner = $(lc_id('number_of_light_cones')).closest('span');
        var maximum = $(lc_id('number_of_light_cones')).data('spin-max');
        if (new_value <= 1) {
            if (new_value <= 0) {
                show_error($spinner, "Please provide a positive number of light-cones");
                fill_in_summary('light_cone', 'number_of_light_cones', 'Negative number of light-cones is invalid');
                return false;
            }
        }

        if ( maximum > 0 ) {
            $(lc_id('number_of_light_cones')).spinner("option", "max", maximum);
            if (new_value >= maximum) {
                if (new_value > maximum) {
                    show_error($spinner, "The maximum is " + maximum);
                    fill_in_summary('light_cone', 'number_of_light_cones', 'Number of light cones selected exceeds the maximum');
                    return false;
                }
            }

        }
        else if (ra != "" && dec != "" && redshift_min != "" && redshift_max != "") {
            show_error($spinner, "Selection parameters can't be used to generate unique light-cones");
            fill_in_summary('light_cone', 'number_of_light_cones', 'An invalid number of light cones is selected');
            return false;
        }

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
                return false;
            }
            else {
                $(lc_id('number_of_light_cones')).spinner("enable");
                $(lc_id('number_of_light_cones')).data("spin-max",maximum);
            }
            spinner_check_value(parseInt($(lc_id('number_of_light_cones')).val()));
            return true;
        }

        var selection = $("input[name='light_cone-light_cone_type']:checked").val();
        if ("unique" == selection) {
            var maximum = get_number_of_unique_light_cones();
            if (spinner_set_max(maximum)) {
                $spinner_label.html("Select the number of light-cones: (maximum for the selected parameters is " + maximum + ")*");
            }
        } else {
            $.ajax({
                url : TAO_JSON_CTX + 'global_parameter/' + 'maximum-random-light-cones',
                dataType: "json",
                error: function() {
                    alert("Couldn't get data for maximum-random-light-cones");
                },
                success: function(data, status, xhr) {
                    var maximum = parseInt(data.fields.parameter_value);
                    if (spinner_set_max(maximum)) {
                        $spinner_label.html("Select the number of light-cones: (maximum " + maximum + " random light-cones)*");
                    }
                }
            });
        }
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

    // - event handlers for fields -
    //
    function init_event_handlers() {

    $(lc_id('ra_opening_angle') + ', ' + lc_id('dec_opening_angle')).change(function(evt){
        fill_in_ra_dec_in_summary();
        calculate_max_number_of_cones();
    });


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


    get_widget().change_event(function(evt){
        update_filter_options(false);

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

    get_widget().option_clicked_event(function(cache_item){
        show_output_property_info(cache_item);
    });

    $(lc_id('dark_matter_simulation')).change(function(evt){
        var $this = $(this);
        var sim_id = $this.val();
        show_simulation_info(sim_id);
        update_galaxy_model_options(sim_id); // triggers galaxy_model.change
    });


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
            fill_in_selection_in_summary();
        }
    });

    $(rf_id('min') + ', ' + rf_id('max')).change(function(evt){
        fill_in_selection_in_summary();
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
            calculate_max_number_of_cones();
        }
    });



    $(lc_id('redshift_min') + ', ' + lc_id('redshift_max')).change(function(evt){
        fill_in_redshift_in_summary();
        calculate_max_number_of_cones();
    });



    $(lc_id('light_cone_type_0')+', '+lc_id('light_cone_type_1')).click(function(evt){
        var $this = $(this);
        fill_in_summary('light_cone', 'light_cone_type', $this.attr('value'));
        calculate_max_number_of_cones();
    });

    $(lc_id('number_of_light_cones')).spinner({
        spin: function(evt, ui) {
            return spinner_check_value(ui.value);
        },
        min: 1
    });

    $(lc_id('number_of_light_cones')).change(function() {
       var new_value = parseInt($(this).val());
       return spinner_check_value(new_value);
    });

    $(lc_id('box_size')).change(function(evt){
        var $this = $(this);
        var box_size_value = parseFloat($this.val());
        var max_box_size = parseFloat($(lc_id('number_of_light_cones')).data("simulation-box-size"));
        if ($this.val() != "" && isNaN(box_size_value)) {
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


    $('#id_output_format-supported_formats').change(function(evt){
        var $this = $(this);
        var output_format_value = $this.find('option:selected').text();
        fill_in_summary('output', 'output_format', output_format_value);
    });


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
        
        var failed = $.validate_all(true);
        if(failed !== undefined) {
            show_tab(failed, 0);
            return false;
        }

        $(lc_id('output_properties')+' option').each(function(i) {
            $(this).attr("selected", "selected");
        });
        $(sed_id('band_pass_filters')+' option').each(function(i) {
            $(this).attr("selected", "selected");
        });
    });

  }

  this.init = function() {

    get_widget().init();
    init_event_handlers();
    
    var init_light_cone_type_value = $('input[name="light_cone-light_cone_type"][checked="checked"]').attr('value');
    fill_in_summary('light_cone', 'number_of_light_cones',  $(lc_id('number_of_light_cones')).val() +  " " + init_light_cone_type_value + " light cones");
    $(lc_id('number_of_light_cones')).attr('class', 'light_cone_field'); // needed to associate the spinner with light-cone only, not when selecting box
    $(lc_id('dark_matter_simulation')).change();
    $(lc_id('galaxy_model')).change();
    $(lc_id('catalogue_geometry')).change();
    $('#id_output_format-supported_formats').change();
    

    $('div.summary_light_cone .output_properties_list').hide();
    $('div.summary_light_cone .simulation_description, div.summary_light_cone .galaxy_model_description').hide();


    fill_in_ra_dec_in_summary();
    fill_in_redshift_in_summary();
    fill_in_summary('light_cone', 'box_size', $(lc_id('box_size')).val());
    fill_in_summary('light_cone', 'snapshot', format_redshift($(lc_id('snapshot')+' option:selected').html()));


  }

    


}
