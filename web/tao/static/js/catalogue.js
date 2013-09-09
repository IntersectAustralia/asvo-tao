
var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};
catalogue._loaded = false;

ko.extenders.logger = function(target, option) {
    target.subscribe(function(newValue) {
       console.log(option + " := ");
       console.log(newValue);
    });
    return target;
};

var TAO_REQUIRED_NO = 'NOT-REQUIRED'; // value not required, no validation necessary
var TAO_REQUIRED_ERROR = 'REQUIRED-ERROR'; // value required and not provided, error
var TAO_REQUIRED_VALIDATE = 'REQUIRED-OK' // value required and provided, must be validated

ko.extenders.required = function(target, option) {

    if (target.hasOwnProperty('required')) {
        throw "Software error: just one required function is allowed"
    }

    var check = typeof option == 'function' ?
        option
        : function() {return option};

    target.required = ko.computed(function(){
        var v = target();
        var required = check();
        if (v === undefined || v === null) {
            return required ? TAO_REQUIRED_ERROR : TAO_REQUIRED_NO;
        }
        if (v.constructor == ''.constructor && v.trim().length == 0) {
            return required ? TAO_REQUIRED_ERROR : TAO_REQUIRED_NO;
        }
        if (v.constructor == [].constructor && v.length == 0) {
            return required ? TAO_REQUIRED_ERROR : TAO_REQUIRED_NO;
        }
        return TAO_REQUIRED_VALIDATE;
    });

    //return the original observable
    return target;

}

ko.extenders.validate = function(target, option) {

    var valid = ko.computed(function(){
        return option(target());
    });

    var old_error;

    if (target.hasOwnProperty('error')) {
        old_error = target.error;
    }

    target.error = ko.computed(function(){
        if (old_error !== undefined) {
            var old = old_error();
            if (old && old.error) return old;
        }
        return valid();
    });
    //return the original observable
    return target;
};

catalogue.validators = {};
catalogue.validators.positive = function(val) {
    var f = parseFloat(val);
    if (isNaN(f))
        return {'error':false};
    if (f <= 0.0)
        return {'error':true, 'message':'This must be positive.'};
    return {'error':false};
};

// Currently is_float really does an is_numeric
catalogue.validators.is_float = function(val) {
    var f = parseFloat(val);
    if (isNaN(f))
        return {'error':true, message:'Please input a number'};
    return {'error':false};
};

catalogue.validators.is_int = function(val) {
    var f = parseInt(val);
    if (isNaN(f))
        return {'error':true, message:'Please input a number'};
    return {'error':false};
};

catalogue.validators.is_numeric = catalogue.validators.is_float;

catalogue.validators._gt = function(v1,v2) {
    return v1 > v2;
}
catalogue.validators._ge = function(v1,v2) {
    return v1 >= v2;
}
catalogue.validators._lt = function(v1,v2) {
    return v1 < v2;
}
catalogue.validators._le = function(v1,v2) {
    return v1 <= v2;
}
catalogue.validators._gen_check_value = function(test, msg) {
    if (!test())
        return {'error':true, 'message': msg};
    return {'error':false};
}
// utility func
catalogue.validators.defined = function(v) {
    return !(v === undefined || v === null || v === ''
        || (typeof v == 'object' && Object.keys(v).length == 0));
}

catalogue.validators._check_value = function(comp_op, v, ref_v, msg) {
    if(!catalogue.validators.defined(ref_v))
        return {'error':false};
    var v1 = parseFloat(v);
    var v2 = parseFloat(ref_v);
    if (isNaN(v1))
        return {'error':true, 'message': 'A number must be provided'};
    if (isNaN(v2))
        return {'error':true, 'message': 'A number to compare to is not defined'};
    if (!comp_op(v1,v2))
        return {'error':true, 'message': msg};
    return {'error':false};
};

catalogue.validators._make_func = function(op, param, base_msg) {
    var check = catalogue.validators._check_value;
    if (typeof param == "function") {
        return function(val) {
            return check(op, val, param(), base_msg + param());
        }
    } else {
        return function(val) {
            return check(op, val, param, base_msg + param);
        }
    }
}

catalogue.validators.geq = function(param, message) {
    var op = catalogue.validators._ge;
    var base_msg = 'Must be greater than or equal to ';
    return catalogue.validators._make_func(op, param, base_msg);
}

catalogue.validators.greater_than = function(param, message) {
    var op = catalogue.validators._gt;
    var base_msg = 'Must be greater than ';
    return catalogue.validators._make_func(op, param, base_msg);
}

catalogue.validators.less_than = function(param, message) {
    var op = catalogue.validators._lt;
    var base_msg = "Must be less than ";
    return catalogue.validators._make_func(op, param, base_msg);
}

catalogue.validators.leq = function(param, message) {
    var op = catalogue.validators._le;
    var base_msg = "Must be less than or equal to ";
    return catalogue.validators._make_func(op, param, base_msg);
}

// generic test (computed observable!) w fixed message
catalogue.validators.test = function(test, message) {
    var gen_check = catalogue.validators._gen_check_value;
    return function(val) {
        return gen_check(test, message);
    }
}



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

var debug_thing = function() {
    console.log('debug');
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

    this.get_observable_by_field = function(field, value, ko_array) {
        var result = null;
        for (var i = 0; i < ko_array().length; i++) {
            if(ko_array()[i]['fields'][field] == value) {
                result = ko_array()[i];
                break;
            }
        }
        return result;
    }

    this.get_observable_by_attribute = function(attr, value, ko_array) {
        var result = null;
        for (var i = 0; i < ko_array().length; i++) {
            if(ko_array()[i][attr] == value) {
                result = ko_array()[i];
                break;
            }
        }
        return result;
    }

    this.get_element_by_attribute = function(attr, value, array) {
        var result = null;
        for (var i = 0; i < array.length; i++) {
            if(array[i][attr] == value) {
                result = array[i];
                break;
            }
        }
        return result;
    }

    this.log_vm = function(msg, vm) {
        var vars = Object.keys(vm);
        ko.utils.arrayForEach(vars, function(var_id){
            var obs = vm[var_id];
            if (ko.isObservable(obs)) {
                obs.subscribe(function(v){
                    console.log([msg, var_id, v])
                });
            }
        });
    }

    // returns a dict with:
    //   required_errors={true|false},
    //   field_errors={true|false},
    //   _errors=array of error messages
    this.validate_vm = function(vm) {
    	// Validate the supplied vm
    	// Iterate over every member and check for errors
    	var attr, obj;
        var _errors = [];
        var required_errors = false;
        var field_errors = false;

    	for (attr in vm) {
    		obj = vm[attr];
            var ui_name = attr;
    		if (obj.hasOwnProperty("error") || obj.hasOwnProperty('required')) {
                var req = undefined;
                if (obj.hasOwnProperty('required')) {
                    req = obj.required();
                } else {
                    var v = obj();
                    req = catalogue.validators.defined(v) ? TAO_REQUIRED_VALIDATE : TAO_REQUIRED_NO;
                }
                switch(req) {
                    case TAO_REQUIRED_NO:
                        break;
                    case TAO_REQUIRED_ERROR:
                        required_errors = true;
                        _errors.push(ui_name + ' is required');
                        break;
                    default:
                        var err = {error: false};
                        if (obj.hasOwnProperty('error')) {
                            err = obj.error();
                        }
                        if (err.error) {
                            field_errors = true;
                            _errors.push(ui_name + ': ' + err.message);
                        }
                }
    		}
            if (obj.hasOwnProperty('validate_array')) {
                var arr = obj();
                for(var i = 0; i < arr.length; i++) {
                    var item_error = that.validate_vm(arr[i]);
                    required_errors = required_errors || item_error.required_errors;
                    field_errors = field_errors || item_error.field_errors;
                    if (item_error._errors.length > 0) {
                        var sub_errors = {item: attr+'['+i+']', errors: item_error._errors};
                        _errors.push(sub_errors);
                    }
                }
            }
    	}
        return {
            _errors: _errors,
            required_errors: required_errors,
            field_errors: field_errors
        };
    }

    this.snapshot = function(id) {
        return $.grep(TaoMetadata.Snapshot, function(elem, idx) { 
            return elem.pk == id
        })[0]
    }

    this.snapshots = function(dsid) {
    	res = $.grep(TaoMetadata.Snapshot, function(elem, idx) {
    		return elem.fields.dataset == dsid;
    	});
    	return res
    }
    
    this.dataset = function(dsid) {
    	// Answer the DataSet object for the given dsid
    	res = $.grep(TaoMetadata.DataSet, function(elem, idx) {
    		return elem.pk == dsid;
    	});
    	return res[0];
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

    this.global_parameter = function(parameter_name) {
        return $.grep(TaoMetadata.GlobalParameter, function(elem, idx) {
            return elem.fields.parameter_name == parameter_name;
        })[0] || {}
    }

    this.global_parameter_or_null = function(parameter_name) {
        params = $.grep(TaoMetadata.GlobalParameter, function(elem, idx) {
            return elem.fields.parameter_name == parameter_name;
        });
        if (params.length != 1) {
        	return null;
        }
        return params[0];
    }


    this.output_choices = function(id, geometry_mask) {
        var resp = $.grep(TaoMetadata.DataSetProperty, function(elem, idx) {
            return elem.fields.dataset == id && elem.fields.is_output && (elem.fields.flags & geometry_mask)
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
        if (this.bandpass_filters._resp === undefined) {
            this.bandpass_filters._resp = gen_pairs(TaoMetadata.BandPassFilter);
        }
        return this.bandpass_filters._resp;
    }
    
    this.bandpass_filter = function(filter_id) {
    	// Lookup the supplied filter.
    	// The id is in the format <pk>_(apparent|absolute)
    	return $.grep(catalogue.util.bandpass_filters(), function(elem, idx) {
    		return elem.pk == filter_id;
    	})[0] || {}
    }


    this.stellar_model = function(id) {
        return $.grep(TaoMetadata.StellarModel, function(elem, idx) { 
            return elem.pk == id
        })[0] || {}
    }

    this.dataset_property = function(id) {
        return $.grep(TaoMetadata.DataSetProperty, function(elem, idx) {
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

    this.submit_job = function() {
	    var job_parameters = {};
    	//
    	// Run each module through:
    	// 1. Cleanup (stuff that isn't required for submission)
    	// 2. Validation
    	// 3. Pre-Submit
    	// Then request job data, collate and submit.
    	//
	    for (var module in catalogue.modules) {
	        console.log('CLEANUP_FIELDS ' + module);
	        catalogue.modules[module].cleanup_fields();
	    }
	
	    var is_valid = true;
	    for (var module in catalogue.modules) {
            var module_vm = catalogue.modules[module].vm;
	        var valid_module = that.validate_vm(module_vm);
	        is_valid = is_valid && valid_module;
	        console.log('IS_VALID ' + module + ': ' + valid_module);
	    }
	
	    if (!is_valid) {
	        console.log('ERROR FOUND');
            // TODO !!! show_tab_error()
	        alert("Validation fails - please check your parameters and try again.")
	        return false;
	    }
	
	    for (var module in catalogue.modules) {
	        catalogue.modules[module].pre_submit();
	    }

	    for (var module in catalogue.modules) {
	    	var module_params;
	    	console.log("Job params for: " + module);
	    	module_params = catalogue.modules[module].job_parameters(); 
	    	jQuery.extend(job_parameters, module_params);
	    };
	    
	    jQuery.extend(job_parameters,
	    		{'job-description': catalogue.vm.description()});
	    catalogue.vm.modal_message("Submitting New Catalogue...");

		$.ajax({
			// TODO: use the current URL, not hard-coded string
			url : TAO_JSON_CTX + '../mock_galaxy_factory/',
			type : 'POST',
			// We only supply simple data types in the parameters,
			// so can use traditional=true when encoding them so the format
			// is the same as the previous form submission.
			data : jQuery.param(job_parameters, true),
			success: function(response, textStatus, jqXHR) {
				if (response.job_submitted) {
					window.open(response.next_page, "_self");
				} else {
					// Save parameters for debugging purposes
					catalogue.last_submit_error = {
							response: response,
							text_status: textStatus,
							jqXHR: jqXHR
					}
					alert("Unexpected error.  Please notify Support.")
				}
			},
			error: function(response, textStatus, jqXHR) {
				// Save parameters for debugging purposes
				catalogue.last_submit_error = {
						response: response,
						text_status: textStatus,
						jqXHR: jqXHR
				}
				if (response.status == 0) {
					// Network error?
					alert("Error during job submission.  Please check your internet connection and try again.");
				} else {
					alert("Error during job submission.\nStatus = " + response.status +
							"\nText = " + response.statusText);
				}
                catalogue.vm.modal_message(null);
			}
		});
	}

}	// End catalog.util

////// summary_submit
catalogue.modules.summary_submit = function ($) {

    // KO ViewModel
    var vm = {}
    this.vm = vm;

    this.cleanup_fields = function () {}

    this.pre_submit = function () {
    }

    this.job_parameters = function() {
    	return {};
    }

    this.init_model = function (init_params) {
        return vm;
    }

}
////// end summary_submit

jQuery(document).ready(function ($) {

    // error : dictionary as returned by computable in check_bind
    function error_display(element, error) {
        var $e = $(element);
        $e.closest('.control-group').removeClass('error');
        $e.popover('destroy');
        $e.closest('.control-group').find('label').removeClass('error');
        switch(error.status) {
            case 'OK':
                break;
            case 'REQUIRED':
                var $label = $e.closest('.control-group').find('label');
                $label.addClass('error');
                break;
            default: /* INVALID */
                $e.closest('.control-group').addClass('error');
                $e.popover({
                    trigger: 'focus',
                    title: 'Validation Error',
                    content: error.message
                });
        }
    }

    function bind_check(element, valueAccessor) {
        var prop = valueAccessor();
        if (prop.hasOwnProperty('required') || prop.hasOwnProperty('error')) {
            var is_required = prop.hasOwnProperty('required');
            var has_error_check =  prop.hasOwnProperty('error');
            var aux = function() {
                var req;
                if (is_required) {
                    req = prop.required();
                } else {
                    req = catalogue.validators.defined(prop()) ? TAO_REQUIRED_VALIDATE : TAO_REQUIRED_NO;
                }
                switch(req) {
                    case TAO_REQUIRED_NO:
                        return {status: 'OK'};
                    case TAO_REQUIRED_ERROR:
                        return {status: 'REQUIRED'};
                    default:
                        var err = {error: false};
                        if (has_error_check) {
                            err = prop.error();
                        }
                        return err.error?
                            {status: 'INVALID', message: err.message}
                            : {status: 'OK'};
                }
            };
            ko.computed(aux).subscribe(function(resp){
                error_display(element, resp);
            });
            error_display(element, aux());
        }
    }


    //
    // KO extension using a jQuery plugin
    //
    ko.bindingHandlers['value'] = (function(ko_value) {

        var pg = {}

        pg.init = function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {

                ko_value.init(element, valueAccessor, allBindingsAccessor);

                bind_check(element, valueAccessor);

            };

        pg.update = function(element, valueAccessor) {

                ko_value.update(element, valueAccessor);

                bind_check(element, valueAccessor);

            };

        return pg;
    })(ko.bindingHandlers['value']);

    ko.bindingHandlers['error_check'] = {
        init : function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
                bind_check(element, valueAccessor);
        }
    };

    ko.bindingHandlers['toggler'] = {
        init: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
            // Make a modified binding context, with a extra properties, and apply it to descendant elements
            var toggler_vm = {

                toggler_text : function(){
                    return toggler_vm.toggler_visible() ? "<<" : ">>"
                },
                toggler_click : function() {
                    toggler_vm.toggler_visible(!toggler_vm.toggler_visible());
                },
                toggler_visible : ko.observable(false)
            };

            var childBindingContext = bindingContext.createChildContext(viewModel);
            ko.utils.extend(childBindingContext, toggler_vm);
            ko.applyBindingsToDescendants(childBindingContext, element);

            // Also tell KO *not* to bind the descendants itself, otherwise they will be bound twice
            return { controlsDescendantBindings: true };
        }
    }

    ko.bindingHandlers['spinner'] = {
        init: function(element, valueAccessor, allBindingsAccessor) {
            //initialize datepicker with some optional options
            var options = ko.computed(function(){
                var resp = allBindingsAccessor().spinnerOptions;
                var min_v = typeof (resp.min || undefined) == 'function' ? resp.min() : (resp.min || NaN);
                var max_v = typeof (resp.max || undefined) == 'function' ? resp.max() : (resp.max || NaN);
                return {min: min_v, max: max_v, disabled: !isNaN(min_v) && !isNaN(max_v) && min_v > max_v};
            });

            $(element).spinner(options());

            //handle the field changing
            ko.utils.registerEventHandler(element, "spinchange", function () {
                var observable = valueAccessor();
                observable($(element).spinner("value"));
            });

            var subscription = options.subscribe(function(newOptions) {
                $(element).spinner(newOptions);
            });

            //handle disposal (if KO removes by the template binding)
            ko.utils.domNodeDisposal.addDisposeCallback(element, function() {
                $(element).spinner("destroy");
                subscription.dispose();
            });

        },
        update: function(element, valueAccessor) {
            var value = ko.utils.unwrapObservable(valueAccessor());

            current = $(element).spinner("value");
            if (value !== current) {
                $(element).spinner("value", value);
            }
        }
    };

    ko.bindingHandlers['tab_handle'] = {
        init: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
            var mod_vm = valueAccessor().model;

            var $e = $(element);
            var $a = $('<a />');
            $a.attr('href','#tabs-' + mod_vm._name);
            $a.attr('id','tao-tabs-' + mod_vm._name);
            $a.text(valueAccessor().label);

            var tab_def = catalogue.tabs_vm.tabs[mod_vm._name];

            var tab_status_ui = function(tab_status) {
                for(var i=0; i<=3; i++) $a.removeClass('status_'+i);
                $a.addClass('status_'+tab_status);
            };

            tab_def.tab_status.subscribe(tab_status_ui);
            tab_def.tab_element = $a;
            tab_def.tab_number = catalogue.tabs_vm._number++;
            catalogue.tabs_vm.tabs_by_number[tab_def.tab_number] = tab_def;

            tab_status_ui(tab_def.tab_status());
            $e.append($a);
        },

        update: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
            // need to do ?
        }
    }

    catalogue.vm = {}

    function manual_modal(message) {
        $('#modal_message_text').val(message);
    }

    function initialise_catalogue_vm_and_tabs(init_params) {
        catalogue.vm.description = ko.observable(init_params.job['job-description']);
        catalogue.vm.modal_message = ko.observable("Loading2...");
        catalogue.vm.modal_message.subscribe(function() {
        	var x, y;

        	if (catalogue.vm.modal_message() == null) return;
        	x = window.innerWidth / 3;
        	y = window.pageYOffset;
            setTimeout(function(){
                console.log("Setting offset to "+x+" "+y);
                $('#modal_message').height($(document).height());
                $('#modal_message_text').offset({
                	top: y+200,
                	left: x});
            }, 200);
        });
        catalogue.tabs_vm = {
            tabs : {},
            tabs_by_number : {},
            _number : 0  // used in tab_handler binding to order tabs by number in the UI
        };
    }

    // Prerequisite: init_model called
    function enrich_enabled(mod_vm) {
        if (mod_vm.hasOwnProperty('enabled')) return;
        var enabled = function() {return true;}
        if (mod_vm.hasOwnProperty('apply_'+ mod_vm._name)) {
            enabled = mod_vm['apply_' + mod_vm._name];
        }
        mod_vm.enabled = enabled;
    }

    // Prerequisite: enrich_enabled for module
    function enrich_error_status(mod_vm) {
        if (mod_vm.hasOwnProperty('error_status'))
            throw 'module implements `error_status` and it should not.';
        mod_vm.error_status = ko.computed(function(){
            if (mod_vm.enabled()) {
                return catalogue.util.validate_vm(mod_vm);
            } else {
                return {required_errors:false, field_errors:false, _errors:[]};
            }
        });
    }

    // Prerequisite: enrich_error_status, enrich_enabled for module
    function enrich_tab(mod_vm) {
        var tab_status_func = function() {
            if (!mod_vm.enabled()) {
                return 0;
            }
            var error_status = mod_vm.error_status();
            if (error_status.field_errors) {
                return 3;
            }
            if (error_status.required_errors) {
                return 2;
            }
            return 1;
        };
        var tabs_vm = catalogue.tabs_vm;
        var tab_def = {
            'tab_number': 0, // ! updated by KO during applyBindings: tab_handler binding
            'tab_status': ko.computed(tab_status_func)
        };
        tabs_vm.tabs[mod_vm._name] = tab_def;
        tab_def.next_tab = function() {
            var next_tab = tabs_vm.tabs_by_number[tab_def.tab_number+1];
            if (next_tab !== undefined)
                next_tab.tab_element.click();
        }
        tab_def.previous_tab = function() {
            var previous_tab = tabs_vm.tabs_by_number[tab_def.tab_number-1];
            if (previous_tab !== undefined)
                previous_tab.tab_element.click();
        }
        tab_def.this_tab = function() {
            tab_def.tab_element.click();
        }
        $.extend(mod_vm, tab_def);
    }

    function initialise_modules(init_params) {
        // create module
        for (var module in catalogue.modules) {
            console.log('Creating module: ' + module)
            catalogue.modules[module] = new catalogue.modules[module]($);
        }
        for (var module in catalogue.modules) {
            console.log('Initialising module: ' + module);
            catalogue.vm[module] = catalogue.modules[module].init_model(init_params);
            catalogue.vm[module]._name = module;
        }
        console.log('Finished module initialisation')
    }

    // the UI requires some properties that we are wiring
    // for the models here
    function prebinding_enrichment() {
        var i = 0;
        for (var module in catalogue.modules) {
            var mod_vm = catalogue.vm[module];
            console.log('enriching ' + module);
            enrich_enabled(mod_vm);
            enrich_error_status(mod_vm);
            enrich_tab(mod_vm);
        }
        catalogue.vm.all_errors = ko.computed(function(){
            var all_errors = [];
            for (var module in catalogue.modules) {
                var mod_vm = catalogue.vm[module];
                var error_status = mod_vm.error_status();
                if (error_status._errors.length > 0) {
                    all_errors.push({
                        'module': module,
                        'errors': error_status._errors
                    });
                }
            }
            return all_errors;
        });
        catalogue.vm.has_errors = ko.computed(function(){
            return catalogue.vm.all_errors().length != 0;
        });
        catalogue.util.show_errors = function() {
            $('#error_report').dialog("open");
        }
        console.log('Finished module enrichment');
    }

    // after KO has done all the binding, we can do
    // some jquery_ui. Use with care! Keep in mind that
    // KO may recreate DOM elements as per UI bindings,
    // so don't do here something that may be changed
    // by KO (unless you ensure KO informs you changes, etc)
    function jquery_ui() {
        var $e = $('#tabs');
        $e.tabs();
        $e.addClass("ui-tabs-vertical ui-helper-clearfix");
        $e.find("li").removeClass("ui-corner-top").addClass("ui-corner-left");
        $('#error_report').dialog({
            resizable: true,
            modal: true,
            autoOpen: false,
            width: 500,
            buttons: {
                Ok: {
                    text: "Ok",
                    id: "id_error_report_ok",
                    click: function() {
                        $(this).dialog("close");
                    }
                }
            }
        });
    }

    (function () {
        catalogue.util = new catalogue.util($);
        var init_params = {
            'job' : TaoJob
        };
        try {
            initialise_catalogue_vm_and_tabs(init_params);
            initialise_modules(init_params);
            prebinding_enrichment();
            ko.applyBindings(catalogue.vm);
            jquery_ui();
            catalogue.vm.modal_message(null);
            catalogue._loaded = true;
        } catch(e) {
            if (e.stack !== undefined) {
                var stack = e.stack.replace(/^[^\(]+?[\n$]/gm, '')
                      .replace(/^\s+at\s+/gm, '')
                      .replace(/^Object.<anonymous>\s*\(/gm, '{anonymous}()@')
                      .split('\n');
                for(var i = 0; i < stack.length; i++) console.log(stack[i]);
            }
            manual_modal('Fatal error initialising the UI, please contact support');
        }
    })();

});
