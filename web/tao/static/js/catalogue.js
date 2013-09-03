
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
        if (!check()) return TAO_REQUIRED_NO;
        var v = target();
        if (v === undefined || v === null || v === '') {
            return TAO_REQUIRED_ERROR;
        }
        if (v.hasOwnProperty('length') && v.length == 0) {
            return TAO_REQUIRED_ERROR;
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

    this.validate_vm = function(vm) {
    	// Validate the supplied vm
    	// Iterate over every member and check for errors
    	var attr, obj;
    	var is_valid = true;

    	for (attr in vm) {
    		obj = vm[attr];
    		if (obj.hasOwnProperty("error") || obj.hasOwnProperty('required')) {
                var valid_field = true;
                if (obj.hasOwnProperty('required')) {
                    var req = obj.required();
                } else {
                    var v = obj();
                    req = catalogue.validators.defined(v) ? TAO_REQUIRED_VALIDATE : TAO_REQUIRED_NO;
                }
                switch(req) {
                    case TAO_REQUIRED_NO:
                        break;
                    case TAO_REQUIRED_ERROR:
                        valid_field = false;
                        break;
                    default:
                        var err = {error: false};
                        if (obj.hasOwnProperty('error')) {
                            err = obj.error();
                        }
                        valid_field = !err.error;
                }
                if (!valid_field) {
                    console.log('error on: ' + attr);
                    is_valid = false;
                    break;
                }
    		}
    	}
    	return is_valid;
    }

    this.validate_error = function(objs) {
    	// Validate the supplied vm
    	// Iterate over every member and check for errors
    	var obj;
    	var is_valid = true;

    	for (var i = 0; i < obs.length; i++) {
    		obj = objs[i];
    		if (obj.hasOwnProperty("error")) {
    			is_valid &= !obj.error().error;
    			if (!is_valid)
    				break;
    		}
    	}
    	return is_valid;
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
	        var valid_module = catalogue.modules[module].validate();
	        is_valid = is_valid && valid_module;
	        console.log('IS_VALID ' + module + ': ' + valid_module);
	    }
	
	    if (!is_valid) {
	        console.log('ERROR FOUND');
	        // show_tab_error();
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

jQuery(document).ready(function ($) {

    // error : dictionary as returned by computable in check_bind
    function error_check(element, error) {
        var $e = $(element);
        $e.closest('.control-group').removeClass('error');
        $e.popover('destroy');
        $e.closest('.control-group').find('span.required').removeClass('error');
        switch(error.status) {
            case 'NOT-REQUIRED':
                break;
            case 'REQUIRED':
                var $star = $e.closest('.control-group').find('span.required');
                $star.addClass('error');
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

    function check_bind(element, valueAccessor) {
        var va = valueAccessor();
        if (va.hasOwnProperty('required') || va.hasOwnProperty('error')) {
            var aux = ko.computed(function(){
                var req;
                if (va.hasOwnProperty('required')) {
                    req = va.required();
                } else {
                    var v = va();
                    req = catalogue.validators.defined(v) ? TAO_REQUIRED_VALIDATE : TAO_REQUIRED_NO;
                }
                switch(req) {
                    case TAO_REQUIRED_NO:
                        return {status: 'NOT-REQUIRED'};
                    case TAO_REQUIRED_ERROR:
                        return {status: 'REQUIRED'}
                    default:
                        var err = {error: false};
                        if (va.hasOwnProperty('error')) {
                            err = va.error();
                        }
                        return err.error?
                            {status: 'INVALID', message: err.message}
                            : {status: 'NOT-REQUIRED'};
                }
            }).subscribe(function(resp){
                error_check(element, resp);
            });
            error_check(element, aux.target());
        }
    }


    //
    // KO extension using a jQuery plugin
    //
    ko.bindingHandlers['value'] = (function(ko_value) {

        var pg = {}

        pg.init = function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {

                ko_value.init(element, valueAccessor, allBindingsAccessor);

                check_bind(element, valueAccessor);

            };

        pg.update = function(element, valueAccessor) {

                ko_value.update(element, valueAccessor);

                check_bind(element, valueAccessor);

            };

        return pg;
    })(ko.bindingHandlers['value']);

    ko.bindingHandlers['error_check'] = {
        init : function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
                check_bind(element, valueAccessor);
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

    ko.bindingHandlers.spinner = {
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

    ko.bindingHandlers['tabs'] = {
        init: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
            var $e = $(element);
            // Make a modified binding context, with a extra properties, and apply it to descendant elements
            var tabs_vm = {
                tabs : {},
                tabs_by_number : {}
            };
            var childBindingContext = bindingContext.createChildContext(viewModel);
            ko.utils.extend(childBindingContext, tabs_vm);
            ko.applyBindingsToDescendants(childBindingContext, element);

            // order is important here; let KO manage/create DOM (above)
            // then we call jQueryUI (below)
            $e.tabs().addClass("ui-tabs-vertical ui-helper-clearfix");
            $e.find("li").removeClass("ui-corner-top").addClass("ui-corner-left");

            // Also tell KO *not* to bind the descendants itself, otherwise they will be bound twice
            var tabs = tabs_vm.tabs_by_number;
            for(var i=0; tabs[i]!==undefined; i++) {
                if (tabs[i].tab_status()!=0) {
                    tabs[i].tab_element.click();
                    break;
                }
            }
            catalogue.tabs_vm = tabs_vm;
            return { controlsDescendantBindings: true };
        }
    }

    ko.bindingHandlers['tab_handle'] = {
        init: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
            var $e = $(element);
            var $a = $('<a />');
            $a.attr('href','#tabs-' + valueAccessor().id);
            $a.attr('id','tao-tabs-' + valueAccessor().id);
            $a.text(valueAccessor().label);
            var tab_def = {
                'tab_element': $a,
                'tab_number': Object.keys(bindingContext.tabs).length,
                'tab_status': ko.observable(0)
            };
            bindingContext.tabs[valueAccessor().id] = tab_def;
            bindingContext.tabs_by_number[tab_def.tab_number] = tab_def;
            $e.append($a);
            tab_def.tab_status.subscribe(function(tab_status){
                for(var i=0;i<=2;i++) {$a.removeClass('status_'+i);}
                $a.addClass('status_'+tab_status);
            });
        },

        update: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
            // need to do ?
        }
    }

    ko.bindingHandlers['tab_form'] = {
        init: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
            $(element).attr('id','tabs-' + valueAccessor().id);
            // Make a modified binding context, with a extra properties, and apply it to descendant elements
            var tabObj = bindingContext.tabs[valueAccessor().id];
            var next_tab = bindingContext.tabs_by_number[tabObj.tab_number+1];
            var previous_tab = bindingContext.tabs_by_number[tabObj.tab_number-1];
            tabObj.next_tab = function() {
                if (next_tab !== undefined)
                    next_tab.tab_element.click();
            }
            tabObj.previous_tab = function() {
                if (previous_tab !== undefined)
                    previous_tab.tab_element.click();
            }
            var childBindingContext = bindingContext.createChildContext(viewModel);
            ko.utils.extend(childBindingContext, tabObj);
            ko.applyBindingsToDescendants(childBindingContext, element);

            // Also tell KO *not* to bind the descendants itself, otherwise they will be bound twice
            return { controlsDescendantBindings: true };
        },

        update: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {

        }
    }

    catalogue.vm = {}

    catalogue.vm.get_tab = function(form) {
        catalogue.modules[form].id;
    }

    function manual_modal(message) {
        $('#modal_message_text').val(message);
    }

    function initialise_modules() {
    	var init_params = {
    			'job' : TaoJob
    	}
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

        for (var module in catalogue.modules) {
            console.log('Creating module: ' + module)
            catalogue.modules[module] = new catalogue.modules[module]($);
        }
        for (var module in catalogue.modules) {
            console.log('Initialising module: ' + module)
            catalogue.vm[module] = catalogue.modules[module].init_model(init_params);
        }

        console.log('Finished module initialisation')
    }

    (function () {
        catalogue.util = new catalogue.util($);
        try {
            initialise_modules();
            ko.applyBindings(catalogue.vm);
            catalogue.vm.modal_message(null);
            catalogue._loaded = true;
        } catch(e) {
            var stack = e.stack.replace(/^[^\(]+?[\n$]/gm, '')
                  .replace(/^\s+at\s+/gm, '')
                  .replace(/^Object.<anonymous>\s*\(/gm, '{anonymous}()@')
                  .split('\n');
            for(var i = 0; i < stack.length; i++) console.log(stack[i]);
            manual_modal('Fatal error initialising the UI, please contact support');
        }
    })();

});
