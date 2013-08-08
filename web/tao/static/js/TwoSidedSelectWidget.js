/**
 * Created with PyCharm.
 * User: cindy
 * Date: 13/02/13
 * Time: 6:20 PM
 */
var TwoSidedSelectWidget = function(elem_id, init_options, to_option) {

    // to_id : id of select element that will be replaced by UI interface
    // to_option : function that given an element of the options_raw array
    //             will return a dictionary with: value, group & text
    var vm = {};

    function a_side_vm(initial_raw, filter) {
        var vm_side = {};

        // helper functions

        var option_click = function(data) {
            vm_side.option_click(data);
        }

        var has_groups = (function (arr) {
            for(var i = 0; i < arr.length; i++)
              if ((typeof to_option(arr[i]).group == 'string') &&
                  to_option(arr[i]).group.length > 0) return true;
            return false;
        })(initial_raw);

        var initial_options = (function(arr) {
            var resp = [];
            for(var i = 0; i < arr.length; i++) {
                var obj = to_option(arr[i]);
                obj.option_click = option_click;
                resp.push(obj);
            }
            return resp;
        })(initial_raw);

        function has_tokens(text, tokens) {
            var token;
            if (typeof text != 'string') return false;
            text = text.toLowerCase();
            for (var j = 0; (token = tokens[j]); j++) {
                if (text.indexOf(token) == -1) {
                    return false;
                }
            }
            return true;
        }

        function filter_option(options) {
            if (!filter) return option;
            var tokens = filter().trim().toLowerCase().split(/\s+/);
            if (tokens.length == 0) return options;
            resp = [];
            for(var i = 0; i < options.length; i++)
                if (has_tokens(options.text, options[i]))
                    resp.push()
        }


        // viewmodel observables

        vm_side.has_groups = has_groups;

        vm_side.options_raw = ko.observableArray(initial_options);

        vm_side.options_total = ko.computed(function(){
            return vm_side.options_raw().length;
        });

        vm_side.clicked_option = ko.observable(undefined);

        vm_side.options = ko.computed(function() {
            if (has_groups) return [];
            if (!filter) return vm_side.options_raw();
            var tokens = filter().trim().toLowerCase().split(/\s+/);
            if (tokens.length == 0) return vm_side.options_raw();
            resp = [];
            var options = vm_side.options_raw();
            for(var i = 0; i < options.length; i++) {
                if (has_tokens(options.text, options[i]))
                    resp.push(options[i]);
            }
            return resp;
        });

        vm_side.option_groups = ko.computed(function(){
            var tokens = filter? filter().trim().toLowerCase().split(/\s+/) : [];

            function filter1(option) {
                if (tokens.length == 0
                    || has_tokens(option.text, tokens)) return option;
                return false;
            }

            var resp = [];
            var group_name_set = {};
            var arr = vm_side.options_raw();
            for(var i = 0; i < arr.length; i++) {
                var option = arr[i];
                var group_name = ((typeof option.group == 'string') &&
                    option.group.length > 0) ? option.group : 'No group';
                var group;
                if (!filter1(option)) continue;
                if (group_name in group_name_set) {
                    group = group_name_set[group_name];
                } else {
                    group = {'group_name': group_name, 'options':[]};
                    group_name_set[group_name] = group;
                    resp.push(group);
                }
                group.options.push(option);
            }
            return resp;
        });

        vm_side.options_selected = ko.observableArray([]);

        // events

        vm_side.option_click = function (data) {
            vm_side.clicked_option(data.value);
        }


        return vm_side;
    }

    function move_data(from_obs, to_obs, criterion) {
        var arr = []
        $.each(from_obs(), function(idx, option) {
            if (option === undefined) return;
            if (criterion(option)) {
                to_obs.push(option);
            } else {
                arr.push(option);
            }
        });
        from_obs(arr);
    }

    vm.id = elem_id.slice(1);
    vm.filter = ko.observable('');
    vm.from_side = a_side_vm(init_options['not_selected'], vm.filter);
    vm.to_side = a_side_vm(init_options['selected'], false);
    vm.op_add = function() {
        var selection = vm.from_side.options_selected();
        if (selection.length == 0) return;
        move_data(vm.from_side.options_raw, vm.to_side.options_raw,
            function(d) { return $.inArray(d.value, selection) != -1});
    };
    vm.op_add_all = function() {
        move_data(vm.from_side.options_raw, vm.to_side.options_raw,
            function(d) { return true});
    };
    vm.op_remove = function() {
        var selection = vm.to_side.options_selected();
        if (selection.length == 0) return;
        move_data(vm.to_side.options_raw, vm.from_side.options_raw,
            function(d) { return $.inArray(d.value, selection) != -1});
    };
    vm.op_remove_all = function() {
        move_data(vm.to_side.options_raw, vm.from_side.options_raw,
            function(d) { return true});
    };

    vm.init = function() {};
    vm.cache_store = function(s) {vm.from_side.options_raw(s)};
    vm.display_selected = function() {};
    vm.change_event = function(f) {};
    vm.option_clicked_event = function(f) {};
    vm.set_enabled = function(v) {};


    return vm;

    /*****
    var $from = $(to_id + '_from');
    var $to = $(to_id);
    var $filter_field = $(to_id + '_filter');
    var $select_option = $(to_id + '_op_add');
    var $remove_option = $(to_id + '_op_remove');
    var $select_all = $(to_id + '_op_add_all');
    var $remove_all = $(to_id + '_op_remove_all');
    var cache = new Array();
    var must_group = false;
    var ref = this;
    var enabled = enable;

    var option_clicked = function(evt) {
        if (ref.option_click_handler) {
            var cache_index = $(evt.target).data('cache_index');
            ref.option_click_handler(cache[cache_index]);
        }
    };

    $(to_id + '-table').resizable({
        maxWidth: $("#tabs-1 > .row-fluid > .boxed.span8").width()
    });

    this.init = function() {

        function status_helper($where, selector, status) {
            var $selected_option = $where.find(selector);
            ref.update_displayed_status($selected_option, status);
            $filter_field.keyup();
            return false;
        }

        $select_option.click(function(e) {
            if (!enabled) {
                e.preventDefault();
            }
            else {
                return status_helper($from, 'option:selected', 2);
            }
        });

        $select_all.click(function(e) {
            if (!enabled) {
                e.preventDefault();
            }
            else {
                return status_helper($from, 'option', 2);
            }
        });

        $remove_option.click(function(e) {
            if (!enabled) {
                e.preventDefault();
            }
            else {
                $filter_field.val('');
                return status_helper($to, 'option:selected', 1);
            }
        });

        $remove_all.click(function(e) {
            if (!enabled) {
                e.preventDefault();
            }
            else {
                $filter_field.val('');
                return status_helper($to, 'option', 1);
            }
        });

        $filter_field.keyup(function(e) {
            $this = $(this);
            var tokens = $this.val().toLowerCase().split(/\s+/);
            console.log('keyup() triggered, tokens: ' + tokens);

            // Redisplay the HTML available select box to display only the choices containing all the words in filter text
            // (i.e. it's an AND search).
            var node;
            for (var i = 0; (node = cache[i]); i++) {
                if (node.displayed == 0) {
                    node.displayed = 1;
                }
            }
            for (var i = 0; (node = cache[i]); i++) {
                if (node.displayed != 2) {
                    for (var j = 0; (token = tokens[j]); j++) {
                        if (node.text.toLowerCase().indexOf(token) == -1) {
                            node.displayed = 0;
                            $(to_id+'_from'+' option[value='+node.value+']').remove();
                        }
                    }
                }
            }
            ref.redisplay(true);
        });
    };

    this.cache_store = function(data) {
        cache = [];
        must_group = false;
        for (var i = 0; i < data.length; i++) {
            var item = data[i];
            cache.push({value: item.pk, text: item.fields.label, description: item.fields.description, displayed: 1, group: item.fields.group});
            must_group = must_group || (typeof(item.fields.group)=="string" && item.fields.group.length > 0);
        }
    };

    this.selected = function() {
        var selected = [];
        for(i=0; i<cache.length; i++) {
            var item = cache[i];
            if (item.displayed == 2) {
                selected.push(item.value + '')
            }
        }
        return selected;
    }

    this.display_selected = function(current, trigger) {
        $filter_field.empty();
        for(i=0; i<cache.length; i++) {
            var item = cache[i];
            if ($.inArray(item.value + '', current) == -1) { // convert to string
                item.displayed = 1;
            } else {
                item.displayed = 2;
            }
        }
        ref.redisplay(trigger);
    };

    this.redisplay = function(trigger) {

        function create_or_current_and_append($group_ptr, name, $option, $side) {
            var $g = null;
            if (($group_ptr[0] == null
                || $group_ptr[0].attr('group-name') != name)
                && must_group ) {
                var $g = $('<optgroup/>');
                $g.attr('group-name', name);
                $g.appendTo($side);
                if (name.length == 0) name = 'Ungrouped';
                $g.attr('label', name);
                $group_ptr[0] = $g;
            } else {
                $g = $group_ptr[0];
            }
            if ($g != null) {
                $option.appendTo($g);
            } else {
                $option.appendTo($side);
            }
        }

        $from.empty();
        $to.empty();

        var $current_group_from = [null];
        var $current_group_to = [null];

        $.each(cache, function(i,v){

            var $option = $('<option/>');
            $option.attr('value', v.value);
            $option.text(v.text);
            $option.data('cache_index', i);
            $option.click(option_clicked);
            if (v.displayed == 1) {
                create_or_current_and_append($current_group_from, v.group, $option, $from);
            }
            if (v.displayed == 2) {
                create_or_current_and_append($current_group_to, v.group, $option, $to);
            }
        });

        if (trigger) {
            $to.change();
        }
    }

    this.change = function() {
        $to.change();
    }

    this.change_event = function(handler) {
        $to.change(handler);
    };

    this.option_clicked_event = function(handler) {
        ref.option_click_handler = handler;
    }

    this.update_displayed_status = function($options, status) {
        var opts = [];
        $options.each(function(){opts.push($(this).attr('value'))});
        $.each(cache, function(i,v){
            if ($.inArray('' + v.value, opts) != -1) {
                cache[i].displayed = status;
            }
        });
    };

    this.set_enabled = function(enable) {
        enabled = enable;
    }
    ****/

}