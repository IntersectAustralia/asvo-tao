/**
 * Created with PyCharm.
 * User: cindy
 * Date: 13/02/13
 * Time: 6:20 PM
 */
var TwoSidedSelectWidget = function(params) {

    // elem_id : id of select element that will be replaced by UI interface (including #)
    // options : observable array with options (read)
    // selectedOption : observable array with selected (write)
    // to_option : function that given an element of the options_raw array
    //             will return a dictionary with: value, group & text

    var elem_id = params['elem_id'];
    var options = params['options'];
    var selectedOptions = params['selectedOptions'];
    var to_option = params['to_option'];

    var vm = {};
    vm.from_side = {};
    vm.to_side = {};

    function option_click(data) {
        vm.option_click(data);
    }

    function make_to_option(selected_observable) {
        var arr = selected_observable();
        return function(obj) {
            var resp = to_option(obj);
            resp['_obj'] = obj;
            resp['_selected'] = $.inArray(obj, arr) != -1;
            resp['option_click'] = option_click;
            return resp;
        }
    }

    function from_selected_option(value){
        return vm._all_by_value[value]._obj;
    }

    function option_order(o1,o2) {
        var c1 = o1.group > o2.group ? 1 : o1.group < o2.group ? -1 : 0;
        if (c1 != 0) return c1;
        c1 = o1.order > o2.order ? 1 : o1.order < o2.order ? -1 : 0;
        if (c1 != 0) return c1;
        return o1.text > o2.text ? 1 : o1.text < o2.text ? -1 : 0;
    };

    function has_groups(arr) {
        var aux = ko.utils.arrayFilter(arr, function(opt){
            return (typeof opt.group == 'string') && opt.group.length > 0;
        });
        return aux.length > 0;
    }

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

    function make_side(is_selected, filter) {

        var vm_side = {};
        vm_side.has_groups = vm.has_groups;
        vm_side.options = ko.computed(function() {
            var tokens = filter().trim().toLowerCase().split(/\s+/);
            var arr = ko.utils.arrayFilter(vm._all_options(), function(opt){
                return opt._selected == is_selected && (tokens.length == 0 || has_tokens(opt.text, tokens));
            });
            return arr;
        });
        vm_side.option_groups = ko.computed(function(){
            var tokens = filter().trim().toLowerCase().split(/\s+/);
            function filter1(opt) {
                return opt._selected == is_selected && (tokens.length == 0 || has_tokens(opt.text, tokens));
            }

            var resp = [];
            var group_name_set = {};
            var arr = vm._all_options();
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

    vm._all_by_value = {};
    vm._all_options = ko.computed(function(){
        var arr = ko.utils.arrayMap(options(), make_to_option(selectedOptions));
        arr.sort(option_order);
        var resp = {};
        for(var i=0; i<arr.length; i++) resp[arr[i].value] = arr[i];
        vm._all_by_value = resp;
        return arr;
    });

    vm.has_groups = ko.observable(has_groups(vm._all_options()));
    vm.id = elem_id.slice(1);
    vm.filter = ko.observable('');

    vm.from_side = make_side(false, vm.filter);
    vm.to_side = make_side(true, function(){return ''});

    vm.clicked_option = ko.observable(undefined);
    vm.option_click = function (data) {
       vm.clicked_option(data.value);
    }

    vm.op_add = function() {
        var selection = ko.utils.arrayMap(vm.from_side.options_selected(), from_selected_option);
        if (selection.length == 0) return;
        selection = selection.concat(selectedOptions());
        selectedOptions(selection);
    };
    vm.op_add_all = function() {
        selectedOptions(options());
        vm.filter('');
    };
    vm.op_remove = function() {
        var selection = ko.utils.arrayMap(vm.to_side.options_selected(), from_selected_option);
        if (selection.length == 0) return;
        var arr = ko.utils.arrayFilter(selectedOptions(), function(obj){
            return $.inArray(obj, selection) == -1;
        })
        selectedOptions(arr);
    };
    vm.op_remove_all = function() {
        selectedOptions([]);
        vm.filter('');
    };

    return vm;

}
