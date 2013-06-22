(function($) {

    var forms = {};
    var all = [];

    function parse(value, type) {
        if(type === 'float')
            return parseFloat(value);
        else if(type === 'int')
            return parseInt(value);
        else
            return value;
    }

    function build_cache(cache) {
        var vals = {}
        for(var key in cache) {
            if(cache.hasOwnProperty(key)) {
                var elem, type;
                if(cache[key] instanceof Array) {
                    elem = cache[key][0];
                    type = cache[key][1];
                }
                else {
                    elem = cache[key];
                    type = undefined;
                }
                vals[key] = parse(elem.val(), type);
            }
        }
        return vals;
    }

    function set_error(elem, msg) {
        elem.closest('.control-group').addClass('error');
        elem.popover({
            trigger: 'focus',
            title: 'Validation Error',
            content: msg
        });
    }

    function clear_error(elem) {
        elem.closest('.control-group').removeClass('error');
        elem.popover('destroy');
        elem.closest('.control-group .help-inline').remove();
    }

    function has_value(elem) {
        if(elem.is('checkbox'))
            return true;
        else {
            var val = elem.val();
            return val !== undefined && val !== null && val != '';
        }
    }

    function validate_element(elem, data, done, force, ev) {
        if(done === undefined)
            done = [];
        done.push(elem);

        // We  only check the element in the following conditions:
        //  1. 'force' is set.
        //  2. We've been called as a result of a focusout.
        //  3. The input is in an error condition.
        //  4. The input has a value.
        if((ev !== undefined && ev.type == 'focusout') ||
           force === true ||
           elem.closest('.control-group').hasClass('error') ||
           has_value(elem)) {

            // First check group elements.
            for(var ii=0; ii<data.group.length; ii++) {
                var grp = data.group[ii];
                if(jQuery.inArray(grp, done) == -1)
                    validate_element(grp, grp.data('validate'), done, force, ev);
            }

            // Now check my element.
            clear_error(elem);
	    if(!elem.is(':disabled')) {
                var cache = build_cache(data.cache);
                var val;
                if(elem.is(':checkbox'))
                    val = elem.is(':checked');
                else {
                    val = elem.val();
                    if(val === undefined || val === null || val == '') {
                        if(data.required) {
                            set_error(elem, 'This value is required.');
                            return false;
                        }
                    }
                    else
                        val = parse(val, data.type);
                }
                for(var ii=0; ii < data.tests.length; ii++) {
		    var test = data.tests[ii];
		    if(!test[0].call(undefined, val, cache, elem)) {
                        set_error(elem, test[1]);
                        return false;
		    }
                }
            }
        }

        return true;
    }

    var methods = {

        init: function(options) {
            return this.each(function() {
                var $this = $(this);

                // Prepare data, if not already done.
                var data = $this.data('validate');
                if(!data) {
                    $this.data('validate', $.extend({
                        type: undefined,
                        cache: {},
                        group: [],
                        form: undefined,
                        required: false
                    }, options));
                    data = $this.data('validate');
                }

                // Make an empty set of tests.
                data.tests = []

                // Upon leaving focus we must run the tests.
                $this.focusout(validate_element.bind(undefined, $this, data, undefined, undefined))

                // If we are identified as part of a form, add it in.
                if(data.form !== undefined) {
                    if(forms[data.form] === undefined)
                        forms[data.form] = []
                    forms[data.form].push($this);
                }

                // Add to the all variable to track everything.
                all.push($this);

                // Remove any inline help.
                $this.closest('.control-group').find('.help-inline').remove();
            });
        },

        destroy: function() {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('validate');
                $(window).unbind('.validate');
                data.validate.remove();
                $this.removeData('validate');
            });
        },

        test: function(options) {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('validate');

                // Append the new test.
                data.tests.push([options.check, options.message])
            });
        }

    }

    jQuery.validate_form = function(form, force) {
	var failed = undefined;
        var done = undefined;
        if(forms[form] !== undefined) {
            for(var ii=0; ii<forms[form].length; ii++) {
                var elem = forms[form][ii];
                var data = elem.data('validate');
                if(data !== undefined)
                    if(!validate_element(elem, data, done, force) && failed === undefined)
			failed = elem;
            }
        }
	return failed;
    }

    jQuery.validate_all = function(force) {
	var failed = undefined;
        var done = undefined;
        for(var ii=0; ii<all.length; ii++) {
            var elem = all[ii];
            var data = elem.data('validate');
            if(data !== undefined)
                if(!validate_element(elem, data, done, force) && failed === undefined)
		    failed = elem;
        }
	return failed;
    }

    $.fn.validate = function(method) {
        if(methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        }
        else if(typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        }
        else {
            $.error('Method ' + method + ' does not exist on jQuery.validate');
        }
    }

}( jQuery ));
