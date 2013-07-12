   // TODO: move all these id functionts to their respective modules

var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};

    var sed_id = function(bare_name) {
    return '#id_sed-' + bare_name;
    }

     var lc_id = function(bare_name) {
        return '#id_light_cone-' + bare_name;
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

    var bound;

    var TAO_NO_FILTER = {'pk':'no_filter', 'type':'X', 'fields':{'label':'No Filter'}};

catalogue.util = function($) {

        this.current_data = undefined;
        this.current_key = null;

    this.fill_in_summary = function(form_name, field_name, input_data) {
        $('div.summary_' + form_name + ' .' + field_name).html(input_data);
    }
    this.clear_in_summary = function(form_name, field_name) {
        $('div.summary_' + form_name + ' .' + field_name).html('None');
    }

    this.list_multiple_selections_in_summary = function(form_name, select_widget){
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

        this.fill_in_summary(form_name, select_widget + '_list', selected_values.join(''));
        console.log("list_multiple_selections_in_summary  " + select_widget + " ends")
        return selections_count;
    }


    this.show_stellar_model_info = function(stellar_id) {
        $.ajax({
            url : TAO_JSON_CTX + 'stellar_model/' + stellar_id,
            dataType: "json",
            error: function(){
                $('div.stellar-model-info').hide();
                alert("Couldn't get data for requested dust model");
            },
            success: function(data, status, xhr) {
                $('div.stellar-model-info .name').html(data.fields.label);
                $('div.stellar-model-info .details').html(data.fields.description);
                $('div.stellar-model-info').show();
                catalogue.util.fill_in_summary('sed', 'stellar_model_description', '<br>' + data.fields.description);
            }
        });
    };

    this.show_output_property_info = function(cache_item) {
        $('div.output-property-info .name').html(cache_item.text);
        $('div.output-property-info .details').html(cache_item.description);
        $('div.output-property-info').show();
    }

    this.clear_info = function(form_name, name) {
        $('div.' + name + '-info .name').html('');
        $('div.' + name + '-info .details').html('');
        $('div.' + name + '-info').show();
    }

    // TODO: This function needs a big re-write to decouple it from all submodules
    this.update_filter_options = function(use_default){
        // TODO: Remove dependency on lc_id
        var data_set_id = $(lc_id('galaxy_model')).val();
        // fetch_data = update_filter_options.current_key != data_set_id;
        fetch_data = this.current_key != data_set_id;


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
            $.each(catalogue.modules.light_cone.lc_output_props_widget.selected(), function(i,value) {
               list.push('D-' + value);
            });
            // TODO: Remove dependency
            if ($(sed_id('apply_sed')).is(':checked')) {
                $.each(catalogue.modules.sed.sed_band_pass_filters_widget.selected(), function(i,value) {
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

        if (!fetch_data) {
            refresh_select(update_filter_options.current_data, use_default);
            return;
        }
        console.log('');
        $.ajax({
            url : TAO_JSON_CTX + 'filters/' + data_set_id,
            dataType: "json",
            error: function() {
                alert("Couldn't get filters");
            },
            success: function(resp, status, xhr) {
                catalogue.util.update_filter_options.current_data = resp;
                catalogue.util.update_filter_options.current_key = data_set_id;
                console.log([catalogue.util.update_filter_options.output_props,
                    catalogue.util.update_filter_options.bandpass_props]);
                if (catalogue.util.update_filter_options.output_props &&
                    catalogue.util.update_filter_options.bandpass_props) {
                    refresh_select(resp, use_default);
                }
            }
        });
    };

    // this.update_filter_options.current_data = undefined;
    // this.update_filter_options.current_key = null;

    this.show_error = function($field, msg) {
        var $enclosing = $field.closest('div.control-group');
        $enclosing.find('span.help-inline').remove();
        $enclosing.removeClass('error');
        if (msg == null) return;
        $field.after('<span class="help-inline"></span>');
        $enclosing.find('span.help-inline').text(msg);
        $enclosing.addClass('error');
        show_tab($enclosing, 0);
    }


    this.validate_min_max = function() {

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

    this.update_filter_options.initializing = true;
    this.update_filter_options.output_props = false;
    this.update_filter_options.bandpass_props = false;

}

jQuery(document).ready(function($) {

    function initialise_modules() {
        for (var module in catalogue.modules) { 
            catalogue.modules[module] = new catalogue.modules[module]($);
        }
        for (var module in catalogue.modules) { 
            catalogue.modules[module].init();
        }
    }

    // focus on tab (direction=0), next tab (direction=+1) or prev tab (direction=-1)
    var show_tab = function($elem, direction) {
        var this_tab = parseInt($elem.closest('div.tao-tab').attr('tao-number'));
        $('#tao-tabs-' + (this_tab + direction)).click();
    }


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
            beforeActivate: catalogue.modules.mock_image.update_tabs
        }).addClass("ui-tabs-vertical ui-helper-clearfix");
        $("#tabs li").removeClass("ui-corner-top").addClass("ui-corner-left");
        // pre-select error
        var $errors = $('div.control-group').filter('.error');
        if ($errors.length > 0) {
            show_tab($errors.first(),0);
        }
    }

    (function(){


        catalogue.util = new catalogue.util($);
        init_wizard();
        initialise_modules();

        console.log('finished module initialization')


    })();
});



