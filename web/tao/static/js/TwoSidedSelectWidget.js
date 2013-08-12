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

    var option_click = function(data) {
        vm.option_click(data);
    }

    function external_to_raw(arr) {
        var resp = [];
        for(var i = 0; i < arr.length; i++) {
            var obj = to_option(arr[i]);
            obj.option_click = option_click;
            resp.push(obj);
        }
        return resp;
    }

    function has_groups(arr) {
        for(var i = 0; i < arr.length; i++)
          if ((typeof to_option(arr[i]).group == 'string') &&
              to_option(arr[i]).group.length > 0) return true;
        return false;
    }

    function a_side_vm(initial_raw, filter) {
        var vm_side = {};

        // helper functions

        var initial_options = external_to_raw(initial_raw);

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
            if (!filter()) return option;
            var tokens = filter().trim().toLowerCase().split(/\s+/);
            if (tokens.length == 0) return options;
            resp = [];
            for(var i = 0; i < options.length; i++)
                if (has_tokens(options.text, options[i]))
                    resp.push()
        }


        // viewmodel observables

        vm_side.has_groups = vm.has_groups;

        vm_side.options_raw = ko.observableArray(initial_options);

        vm_side.options_total = ko.computed(function(){
            return vm_side.options_raw().length;
        });

        vm_side.options = ko.computed(function() {
            if (vm.has_groups()) return [];
            if (!filter()) return vm_side.options_raw();
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
            var tokens = filter()? filter().trim().toLowerCase().split(/\s+/) : [];

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
    vm.has_groups = ko.observable(has_groups(init_options['not_selected'].concat(init_options['selected'])));
    vm.from_side = a_side_vm(init_options['not_selected'], vm.filter);
    vm.to_side = a_side_vm(init_options['selected'], ko.observable(false));
    vm.clicked_option = ko.observable(undefined);
    vm.option_click = function (data) {
       vm.clicked_option(data.value);
    }


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

    vm.new_options = function(objs) {
        vm.has_groups(has_groups(objs));
        vm.from_side.options_raw(external_to_raw(objs));
        vm.to_side.options_raw([]);
    }

    vm.init = function() {};
    vm.cache_store = function(s) {vm.from_side.options_raw(s)};
    vm.display_selected = function() {};
    vm.change_event = function(f) {};
    vm.option_clicked_event = function(f) {};
    vm.set_enabled = function(v) {};


    return vm;

}