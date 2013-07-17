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


    var get_tab_number = function($elem) {
        return parseInt($elem.closest('div.tao-tab').attr('tao-number'));
    }

    // focus on tab (direction=0), next tab (direction=+1) or prev tab (direction=-1)
    this.show_tab = function($elem, direction) {
        var this_tab = get_tab_number($elem);
        $('#tao-tabs-' + (this_tab + direction)).click();
    }

    this.show_error = function($field, msg) {
        var $enclosing = $field.closest('div.control-group');
        $enclosing.find('span.help-inline').remove();
        $enclosing.removeClass('error');
        if (msg == null) return;
        $field.after('<span class="help-inline"></span>');
        $enclosing.find('span.help-inline').text(msg);
        $enclosing.addClass('error');
        this.show_tab($enclosing, 0);
    }


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


    var show_tab_error = function() {
        var $errors = $('div.control-group').filter('.error');
        if ($errors.length > 0) {
            catalogue.util.show_tab($errors.first(),0);
        }
    }


    function init() {
        function set_click(selector, direction) {
            $(selector).click(function(evt) {
                var $this = $(this);
                catalogue.util.show_tab($this, direction);
            })
        }
        set_click('.tao-prev', -1);
        set_click('.tao-next', +1);
        $("#tabs").tabs({
            beforeActivate: catalogue.modules.mock_image.update_tabs
        }).addClass("ui-tabs-vertical ui-helper-clearfix");
        $("#tabs li").removeClass("ui-corner-top").addClass("ui-corner-left");
        // pre-select error
        show_tab_error();

        //
        // -- form handler
        //
        $('#mgf-form').submit(function(){
            var $form = $(this);

            for (var module in catalogue.modules) { 
                console.log('CLEANUP_FIELDS ' + module);
                catalogue.modules[module].cleanup_fields($form);
            }

            var is_valid = true;
            for (var module in catalogue.modules) { 
                console.log('IS_VALID ' + module);
                is_valid = is_valid && catalogue.modules[module].validate($form);
            }

            if(!is_valid) {
                console.log('ERROR FOUND');
                show_tab_error();
                return false;
            }

            for (var module in catalogue.modules) { 
                catalogue.modules[module].pre_submit($form);
            }
        });

    }

    (function(){

        catalogue.util = new catalogue.util($);
        init();
        initialise_modules();

        console.log('Finished module initialisation')


    })();
});



