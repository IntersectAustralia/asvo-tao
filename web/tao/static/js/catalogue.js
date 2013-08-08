
var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};


// TODO: at some point these should be moved to (or at least declared in) their respective modules

var sed_id = function (bare_name) {
    return '#id_sed-' + bare_name;
}


var lc_id = function (bare_name) {
    return '#id_light_cone-' + bare_name;
};


var mi_id = function (bare_name) {
    return '#id_mock_image-' + bare_name;
};


var rf_id = function (bare_name) {
    return '#id_record_filter-' + bare_name;
}


var item_to_value = function (item) {
    return item.type + '-' + item.pk;
}


var bound;


var TAO_NO_FILTER = {
    'pk': 'no_filter',
    'type': 'X',
    'fields': {
        'label': 'No Filter'
    }
};

function set_error($elem, msg) {
    $elem.closest('.control-group').addClass('error');
    $elem.popover({
        trigger: 'focus',
        title: 'Validation Error',
        content: msg
    });
}

function clear_error($elem) {
    $elem.closest('.control-group').removeClass('error');
    $elem.popover('destroy');
    $elem.closest('.control-group .help-inline').remove();
}

function clean_inline($elem) {
    $elem.closest('.control-group').find('.help-inline').remove();
}

function has_value($elem) {
    if($elem.is('checkbox'))
        return true;
    else {
        var val = $elem.val();
        return val !== undefined && val !== null && val != '';
    }
}



catalogue.util = function ($) {

    this.current_data = undefined;
    this.current_key = null;

    var that = this;

    this.snapshots = function(sid, gid) {
        // Answer the Snapshots (redshifts) matching for the supplied dataset , identified
        // by Simulation ID & Galaxy Model ID
    	var dsid;
    	var res;
    	console.log('catalogue.util.snapshots(sid=' + sid + ', gid=' + gid +')')
    	//debugger;
        dsid = $.grep(TaoMetadata.DataSet, function(elem, idx) { 
            return elem.fields.simulation == sid && 
            	elem.fields.galaxy_model == gid 
        })[0].pk;
    	console.log('catalogue.util.snapshots: dsid=' + dsid)
    	res = $.grep(TaoMetadata.Snapshot, function(elem, idx) {
    		return elem.fields.dataset == dsid;
    	});
    	console.log('Length: ' + res.length)
    	return res
    }

    this.simulation = function(id) {
        return $.grep(TaoMetadata.Simulation, function(elem, idx) { 
            return elem.pk == id
        })[0]
    }


    this.galaxy_model = function(id) {
        return $.grep(TaoMetadata.GalaxyModel, function(elem, idx) { 
            return elem.pk == id
        })[0]
    }


    this.galaxy_models = function(sid) {
        var datasets = $.grep(TaoMetadata.DataSet, function(elem, idx) { 
            return elem.fields.simulation == sid 
        });
        return $.map(datasets, function(elem, idx) {
            var gm = that.galaxy_model(elem.fields.galaxy_model); 
            return {'id':elem.pk, 
            'name':gm.fields.name, 
            'galaxy_model_id':elem.fields.galaxy_model, 
            'job_size_p1': elem.fields.job_size_p1,
            'job_size_p2': elem.fields.job_size_p2,
            'job_size_p3': elem.fields.job_size_p3,
            'max_job_box_count': elem.fields.max_job_box_count}
        });
    }


    this.global_parameter = function(parameter_name) {
        return $.grep(TaoMetadata.GlobalParameter, function(elem, idx) {
            return elem.fields.parameter_name == parameter_name;
        })[0] || {}
    }


    this.output_choices = function(id) {
        var resp = $.grep(TaoMetadata.DataSetProperty, function(elem, idx) { 
            return elem.fields.dataset == id && elem.fields.is_output
        });
        return resp.sort(function (a, b) {
            if (a.fields.group != b.fields.group)
                return a.fields.group < b.fields.group ? -1 : 1;
            if (a.fields.order != b.fields.order)
                return a.fields.order < b.fields.order ? -1 : 1;
            if (a.fields.label != b.fields.label)
                return a.fields.label < b.fields.label ? -1 : 1;            
            return 0;
        });
    }


    this.dust_model = function(id) {
        return $.grep(TaoMetadata.DustModel, function(elem, idx) { 
            return elem.pk == id
        })[0] || {}
    }


    this.bandpass_filters = function() {
        var gen_pairs = function(bandpass_filters) {
            function gen_dict(elem, extension) {
                return {
                    "pk": elem.pk + '_' + extension,
                    "model": "tao.bandpassfilter",
                    "fields": {
                        "order": elem.fields.order,
                        "filter_id": elem.fields.filter_id,
                        "group": elem.fields.group,
                        "description": elem.fields.description,
                        "label": elem.fields.label + ' (' + extension.charAt(0).toUpperCase() + extension.slice(1) + ')'
                    }
                };
            }
            return $.map(bandpass_filters, function(elem, idx) {
                return [gen_dict(elem, 'apparent'), gen_dict(elem, 'absolute')]
            });
        }
        return gen_pairs(TaoMetadata.BandPassFilter);
    }


    this.stellar_model = function(id) {
        return $.grep(TaoMetadata.StellarModel, function(elem, idx) { 
            return elem.pk == id
        })[0] || {}
    }


    this.filters = function(id) {
        var data_set = $.grep(TaoMetadata.DataSet, function(elem, idx) { 
            return elem.pk == id
        })[0] || {};

        var json_my_encode = function(obj, extension) {
            if (obj.model == 'tao.datasetproperty') {
                return {
                    'type':'D',
                    'pk':obj.pk, 
                    'fields': {
                        'name':obj.fields.name,
                        'units':obj.fields.units,
                        'label':obj.fields.label,
                        'data_type':obj.fields.data_type
                    }}
            } else if (obj.model == 'tao.bandpassfilter') {
                return {
                    'type':'B',
                    'pk': obj.pk + '_' + extension,
                    'fields': {
                        'name':obj.fields.filter_id,
                        'units':'',
                        'label':obj.fields.label + ' (' + extension.charAt(0).toUpperCase() + extension.slice(1) + ')',
                        'data_type': 1
                    }}
            } else {
                throw obj.model + " is not JSON known as filter property"
            }
        };

        var gen_pairs = function(bandpass_filters) {
            return $.map(bandpass_filters, function(elem, idx) {
                return [json_my_encode(elem, 'apparent'), json_my_encode(elem, 'absolute')]
            });
        };

        var filter_choices = function() {
            var filters = $.grep(TaoMetadata.DataSetProperty, function(elem, idx){
                return elem.fields.dataset == data_set.pk && 
                (elem.fields.is_filter || elem.pk === data_set.fields.default_filter_field)
            });
            return $.map(filters, function(elem, idx){
                return json_my_encode(elem);
            });  
        }
        

        return {
            'list': $.merge(filter_choices(), gen_pairs(TaoMetadata.BandPassFilter)),
            'default_id': data_set.pk,
            'default_min': data_set.fields.default_filter_min,
            'default_max': data_set.fields.default_filter_max
        }
    }


    this.fill_in_summary = function (form_name, field_name, input_data) {
        $('div.summary_' + form_name + ' .' + field_name).html(input_data);
    }


    this.clear_in_summary = function (form_name, field_name) {
        $('div.summary_' + form_name + ' .' + field_name).html('None');
    }


    this.list_multiple_selections_in_summary = function (form_name, select_widget) {
        console.log("list_multiple_selections_in_summary for " + select_widget + " starts")
        var selections_count = 0;
        var selected_values = [];

        selected_values.push('<ul>');
        var $groups = $('#id_' + form_name + '-' + select_widget + ' optgroup');
        console.log(form_name + ' ' + select_widget + ' has group size: ' + $groups.size());
        if ($groups.size() > 0) {
            $groups.each(function (i, e) {
                var name = $(e).attr('group-name');
                if (name.length == 0) {
                    name = "Ungrouped";
                }
                selected_values.push('<li>' + name + '<ul>');
                $(e).find('option').each(function (i, option) {
                    selected_values.push('<li>' + $(option).html() + '</li>');
                    selections_count++;
                })
                selected_values.push('</ul></li>');
            })
        } else {
            $('#id_' + form_name + '-' + select_widget + ' option').each(function (i, option) {
                selected_values.push('<li>' + $(option).html() + '</li>');
                selections_count++;
            });
        }
        selected_values.push('</ul>');

        this.fill_in_summary(form_name, select_widget + '_list', selected_values.join(''));
        console.log("list_multiple_selections_in_summary  " + select_widget + " ends")
        return selections_count;
    }


    this.show_stellar_model_info = function (stellar_id) {
        var data = catalogue.util.stellar_model(stellar_id);
        $('div.stellar-model-info .name').html(data.fields.label);
        $('div.stellar-model-info .details').html(data.fields.description);
        $('div.stellar-model-info').show();
        catalogue.util.fill_in_summary('sed', 'stellar_model_description', '<br>' + data.fields.description);
        // $.ajax({
        //     url: TAO_JSON_CTX + 'stellar_model/' + stellar_id,
        //     dataType: "json",
        //     error: function () {
        //         $('div.stellar-model-info').hide();
        //         alert("Couldn't get data for requested dust model");
        //     },
        //     success: function (data, status, xhr) {
        //         $('div.stellar-model-info .name').html(data.fields.label);
        //         $('div.stellar-model-info .details').html(data.fields.description);
        //         $('div.stellar-model-info').show();
        //         catalogue.util.fill_in_summary('sed', 'stellar_model_description', '<br>' + data.fields.description);
        //     }
        // });
    };


    this.show_output_property_info = function (cache_item) {
        $('div.output-property-info .name').html(cache_item.text);
        $('div.output-property-info .details').html(cache_item.description);
        $('div.output-property-info').show();
    }


    this.clear_info = function (form_name, name) {
        $('div.' + name + '-info .name').html('');
        $('div.' + name + '-info .details').html('');
        $('div.' + name + '-info').show();
    }


    var get_tab_number = function ($elem) {
        return parseInt($elem.closest('div.tao-tab').attr('tao-number'));
    }


    // focus on tab (direction=0), next tab (direction=+1) or prev tab (direction=-1)
    this.show_tab = function ($elem, direction) {
        var this_tab = get_tab_number($elem);
        $('#tao-tabs-' + (this_tab + direction)).click();
    }


    this.show_error = function ($field, msg) {
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


jQuery(document).ready(function ($) {

    function initialise_modules() {
        for (var module in catalogue.modules) {
            console.log('Creating module: ' + module)
            catalogue.modules[module] = new catalogue.modules[module]($);
        }
        for (var module in catalogue.modules) {
            console.log('Initialising module: ' + module)
            if (module=='light_cone') {
                catalogue.modules[module].init_model();
                catalogue.modules[module].init_ui();
                catalogue.modules[module].chain_events();
            } else {
                catalogue.modules[module].init();
            }
        }
        console.log('Finished module initialisation')
    }


    var show_tab_error = function () {
        var $errors = $('div.control-group').filter('.error');
        if ($errors.length > 0) {
            catalogue.util.show_tab($errors.first(), 0);
        }
    }


    function init() {

        function setup_editable_text(elem_id) {
            var $elem = $(elem_id);

            $('#id-save_edit').click(function(evt){
                var description = $elem.text().replace(/\s+/g, ' ');
                $.ajax({
                    url: TAO_JSON_CTX + 'edit_job_description/' + $('#csrf_token #job_id').val(),
                    type: 'POST',
                    data: {"job-description": description,
                        'csrfmiddlewaretoken': $('#csrf_token input[name="csrfmiddlewaretoken"]').val()},
                    error: function(data) {
                        alert("Couldn't save job description to DB");
                    }
                });
            });

            $('#id-cancel_edit').click(function(evt){
                document.execCommand('undo', false, null);
            });
        }

        setup_editable_text('#id-job_description');

        function set_click(selector, direction) {
            $(selector).click(function (evt) {
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
        $('#mgf-form').submit(function () {
            var $form = $(this);

            for (var module in catalogue.modules) {
                console.log('CLEANUP_FIELDS ' + module);
                catalogue.modules[module].cleanup_fields($form);
            }

            var is_valid = true;
            for (var module in catalogue.modules) {
                var valid_module = catalogue.modules[module].validate($form);
                is_valid = is_valid && valid_module;
                console.log('IS_VALID ' + module + ': ' + valid_module);
            }

            if (!is_valid) {
                console.log('ERROR FOUND');
                show_tab_error();
                return false;
            }

            for (var module in catalogue.modules) {
                catalogue.modules[module].pre_submit($form);
            }
        });

    }


    (function () {
        catalogue.util = new catalogue.util($);
        init();
        initialise_modules();
    })();

});
