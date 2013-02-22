/**
 * Created with PyCharm.
 * User: cindy
 * Date: 13/02/13
 * Time: 6:20 PM
 */
var TwoSidedSelectWidget = function(to_id, enable) {
    var $from = $(to_id + '_from');
    var $to = $(to_id);
    var $filter_field = $(to_id + '_filter');
    var $select_option = $(to_id + '_op_add');
    var $remove_option = $(to_id + '_op_remove');
    var $select_all = $(to_id + '_op_add_all');
    var $remove_all = $(to_id + '_op_remove_all');
    var cache = new Array();
    var ref = this;
    var enabled = enable;

    this.init = function() {

        var resize_filters = function() {
            $to.height($filter_field.outerHeight() + $from.outerHeight() + 3);
            $filter_field.width($from.innerWidth() - 11);
        }
        resize_filters();

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
                console.log('node value=' + node.value + ' node.text=' + node.text + ' displayed=' + node.displayed);
            }
            ref.redisplay();
        });
    };

    this.cache_store = function(data) {
        cache = [];
        for (var i = 0; i < data.length; i++) {
            var item = data[i];
            cache.push({value: item.pk, text: item.fields.name, displayed: 1});
        }
    };

    this.display_selected = function(current) {
        $filter_field.empty();
        for(i=0; i<cache.length; i++) {
            var item = cache[i];
            if ($.inArray(item.value + '', current) == -1) { // convert to string
                item.displayed = 1;
            } else {
                item.displayed = 2;
            }
        }
        ref.redisplay();
    };

    this.redisplay = function() {
        $from.empty();
        $to.empty();
        $.each(cache, function(i,v){
            var $option = $('<option/>');
            $option.attr('value', v.value);
            $option.text(v.text);
            if (v.displayed == 1) {
                $option.appendTo($from);
            }
            if (v.displayed == 2) {
                $option.appendTo($to);
            }
        });
        $to.change();
    }

    this.change_event = function(handler) {
        $to.change(handler);
    };

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

    this.init();

}