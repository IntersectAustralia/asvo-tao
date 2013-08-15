
var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};


ko.extenders.logger = function(target, option) {
    target.subscribe(function(newValue) {
       console.log(option + " := ");
       console.log(newValue);
    });
    return target;
};

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
    if(val === undefined || val === null || val == '')
        return {'error':false};
    var f = parseFloat(val);
    if (isNaN(f))
        return {'error':false};
    if (f <= 0.0)
        return {'error':true, 'message':'This must be positive.'};
    return {'error':false};
};

// Currently is_float really does an is_numeric
catalogue.validators.is_float = function(val) {
    if(val === undefined || val === null || val == '')
        return {'error':false};
    var f = parseFloat(val);
    if (isNaN(f))
        return {'error':true, message:'Please input a number'};
    return {'error':false};
};

catalogue.validators.is_int = function(val) {
    if(val === undefined || val === null || val == '')
        return {'error':false};
    var f = parseInt(val);
    if (isNaN(f))
        return {'error':true, message:'Please input a number'};
    return {'error':false};
};

catalogue.validators.is_numeric = catalogue.validators.is_float;

catalogue.validators.greater_than = function(param) {
    function check(v, min_v, msg) {
        if(v === undefined || v === null || v === ''
           || min_v === undefined || min_v === null || v === '')
            return {'error':false};
        var f = parseFloat(v);
        if (isNaN(f) || isNaN(parseFloat(min_v)))
            return {'error':false};
        if (f < parseFloat(min_v))
            return {'error':true, 'message': msg};
        return {'error':false};
    }
    if (typeof param == "function") {
        return function(val) {
            return check(val, param(), 'Must be greater than ' + param());
        }
    } else {
        return function(val) {
            return check(val, param, 'Must be greater than ' + param);
        }
    }
}

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
    return !(v === undefined || v === null || v === '');
}

catalogue.validators.is_ok = function(obs) {
    if (!catalogue.validators.defined(obs()))
        return false;
    if (obj.hasOwnProperty("error")) {
        return !obs.error().error;
    }
    return true;
}

catalogue.validators._check_value = function(comp_op, v, ref_v, msg) {
    if(v === undefined || v === null || v === ''
       || ref_v === undefined || ref_v === null || ref_v === '')
        return {'error':false};
    var v1 = parseFloat(v);
    var v2 = parseFloat(ref_v);
    if (isNaN(v1) || isNaN(v2))
        return {'error':false};
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

    this.validate_vm = function(vm) {
    	// Validate the supplied vm
    	// Iterate over every member and check for errors
    	var attr, obj;
    	var is_valid = true;

    	for (attr in vm) {
    		obj = vm[attr];
    		if (obj.hasOwnProperty("error")) {
    			is_valid &= !obj.error().error;
    			if (!is_valid)
    				break;
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
			url : '/mock_galaxy_factory/',
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
                                catalogue.modal_message(null);
			}
		});
	}

}	// End catalog.util

jQuery(document).ready(function ($) {

    //
    // KO extension using a jQuery plugin
    //
    ko.bindingHandlers['value'] = (function(ko_value) {

        function error_check(element, error) {
            var $e = $(element);
            $e.closest('.control-group').removeClass('error');
            $e.popover('destroy');
            $e.closest('.control-group .help-inline').remove();
            if (error && error.error) {
                $e.closest('.control-group').addClass('error');
                $e.popover({
                    trigger: 'focus',
                    title: 'Validation Error',
                    content: error.message
                });
            }
        }

        var pg = {}

        pg.init = function(element, valueAccessor, allBindingsAccessor) {

                ko_value.init(element, valueAccessor, allBindingsAccessor);

                // This will be called when the binding is first applied to an element
                // Set up any initial state, event handlers, etc. here
                var va = valueAccessor();
                if (!(va.hasOwnProperty('error'))) return;
                va.error.subscribe(function(){
                    error_check(element, va.error());
                });
            };

        pg.update = function(element, valueAccessor) {

                ko_value.update(element, valueAccessor);

                var va = valueAccessor();
                if (!(va.hasOwnProperty('error'))) return;

                error_check(element, va.error());

            };

        return pg;
    })(ko.bindingHandlers['value']);

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


    catalogue.vm = {}

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
                $('#modal_message').height(document.height);
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


    var show_tab_error = function () {
        var $errors = $('div.control-group').filter('.error');
        if ($errors.length > 0) {
            catalogue.util.show_tab($errors.first(), 0);
        }
    }


    function init() {

        function set_click(selector, direction) {
            $(selector).click(function (evt) {
                var $this = $(this);
                catalogue.util.show_tab($this, direction);
            })
        }

        
        set_click('.tao-prev', -1);
        set_click('.tao-next', +1);
        $("#tabs").tabs().addClass("ui-tabs-vertical ui-helper-clearfix");
        $("#tabs li").removeClass("ui-corner-top").addClass("ui-corner-left");
        // pre-select error
        show_tab_error();

    }


    (function () {
        catalogue.util = new catalogue.util($);
        initialise_modules();
        init();
        ko.applyBindings(catalogue.vm);
        catalogue.vm.modal_message(null);

    })();

});
