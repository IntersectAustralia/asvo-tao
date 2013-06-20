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
    }

    function validate_element(elem, data, done) {
        if(done === undefined)
            done = [];
        done.push(elem);

        // First check group elements.
        for(var ii=0; ii<data.group.length; ii++) {
            var grp = data.group[ii];
            if(jQuery.inArray(grp, done) == -1)
                validate_element(grp, grp.data('validate'), done);
        }

        // Now check my element.
        clear_error(elem);
        var cache = build_cache(data.cache);
        var val = parse(elem.val(), data.type);
        for(var ii=0; ii < data.tests.length; ii++) {
            var test = data.tests[ii];
            if(!test[0].call(undefined, val, cache, elem)) {
                set_error(elem, test[1]);
                return false;
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
                        form: undefined
                    }, options));
                    data = $this.data('validate');
                }

                // Make an empty set of tests.
                data.tests = []

                // Upon leaving focus we must run the tests.
                $this.focusout(validate_element.bind(undefined, $this, data, undefined))

                // If we are identified as part of a form, add it in.
                if(data.form !== undefined) {
                    if(forms[data.form] === undefined)
                        forms[data.form] = []
                    forms[data.form].push($this);
                }

                // Add to the all variable to track everything.
                all.push($this);
            });
        },

        destroy: function() {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('validate');

                // Remove the element from the all array.
                var idx = jQuery.inArray($this, all);
                if(idx > -1)
                    all.splice(idx, 1);

                // Remove the element from any forms.
                for(var key in forms) {
                    idx = jQuery.inArray($this, forms[key]);
                    if(idx > -1) {
                        forms[key].splice(idx, 1);
                        if(forms[key].length == 0)
                            delete forms[key];
                    }
                }

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

    jQuery.validate_form = function(form) {
        var done = undefined;
        if(forms[form] !== undefined) {
            for(var ii=0; ii<forms[form].length; ii++) {
                var elem = forms[form][ii];
                validate_element(elem, elem.data('validate'), done);
            }
        }
    }

    jQuery.validate_all = function() {
        var done = undefined;
        for(var ii=0; ii<all.length; ii++) {
            var elem = all[ii];
            validate_element(elem, elem.data('validate'), done);
        }
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
