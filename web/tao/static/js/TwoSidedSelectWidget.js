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
    var must_group = false;
    var ref = this;
    var enabled = enable;
    var $drag = $(to_id + '_drag');

    var option_clicked = function(evt) {
        if (ref.option_click_handler) {
            var cache_index = $(evt.target).data('cache_index');
            ref.option_click_handler(cache[cache_index]);
        }
    };


//    $(to_id + ' td').each(function(i,n){
//        $(n).resizable({
//            alsoResize: $(n).parent()
//        });
//    });
//    $(to_id + ' tr').resizable({
//        handles: "e",
//
//        //set correct COL element and original size
//        start: function(event, ui) {
//            var colIndex = ui.helper.index() + 1;
//            colElement = table.find("colgroup > col:nth-child(" + colIndex + ")");
//            //get col width
//            colWidth = parseInt(colElement.get(0).style.width, 10);
//            originalSize = ui.size.width;
//        },
//
//        //set COL width
//        resize: function(event, ui) {
//            var resizeDelta = ui.size.width - originalSize;
//            var newColWidth = colWidth + resizeDelta;
//            colElement.width(newColWidth);
//        }
//    });
    // todo: refactor this
//    var boxWidth = $("#tabs-1 > .row-fluid > .boxed.span8").width();
//    $(window).resize(function(){
//        boxWidth = $("#tabs-1 > .row-fluid > .boxed.span8").width();
//    });
//
    $(to_id + '-table').resizable({
        maxWidth: $("#tabs-1 > .row-fluid > .boxed.span8").width()
    });


    this.init = function() {
//        var resize_filters = function() {
//            $to.height($filter_field.outerHeight() + $from.outerHeight() + 3);
//            $filter_field.width($from.innerWidth() - 11);
//        }
//        resize_filters();

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
//                console.log('node value=' + node.value + ' node.text=' + node.text + ' displayed=' + node.displayed);
            }
            ref.redisplay(true);
        });
    };

    this.resize_widget = function() {
        var table_height = $(to_id + '-table').innerHeight();
        $from.height(table_height-$filter_field.outerHeight());
        $to.height($filter_field.outerHeight() + $from.outerHeight() + 5);
        var right_cell_width = $(to_id + '-right').innerWidth();
        $to.width(right_cell_width);
        var left_cell_width = $(to_id + '-left').innerHeight();
        $filter_field.width(left_cell_width);
        $from.width(left_cell_width);
    };
    this.resize_widget();

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
            if (($group_ptr[0] == null /* first time */
                || $group_ptr[0].attr('group-name') != name /* current is not same */)
                && must_group /* have to create */) {
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

    this.init();

}