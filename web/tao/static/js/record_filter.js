var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};

catalogue.modules.record_filter = function($) {

    console.log('new record_filter module');

	function me() {
		return catalogue.modules.record_filter;
	}

    var fill_in_selection_in_summary = function() {
        var filter_min = $(rf_id('min')).val();
        var filter_max = $(rf_id('max')).val();
        var filter_selected = $(rf_id('filter')).find('option:selected').html();
        if (!filter_min && !filter_max)
            catalogue.util.fill_in_summary ('record_filter', 'record_filter', filter_selected);
        else if (!filter_min)
            catalogue.util.fill_in_summary ('record_filter', 'record_filter', filter_selected + ' &le; ' + filter_max);
        else if (!filter_max)
            catalogue.util.fill_in_summary ('record_filter', 'record_filter', filter_min + ' &le; ' + filter_selected);
        else
            catalogue.util.fill_in_summary ('record_filter', 'record_filter', filter_min + ' &le; ' + filter_selected + ' &le; ' + filter_max);
    }

  function init_event_handlers() {
  	$(rf_id('filter')).change(function(evt){
	    var $this = $(this);
	    var filter_value = $this.val();
	    if (filter_value == item_to_value(TAO_NO_FILTER)) {
	        $(rf_id('max')).attr('disabled', 'disabled');
	        $(rf_id('min')).attr('disabled', 'disabled')
	        catalogue.util.fill_in_summary ('record_filter', 'record_filter', 'No Filter');
	    } else {
	        $(rf_id('max')).removeAttr('disabled');
	        $(rf_id('min')).removeAttr('disabled');
	        fill_in_selection_in_summary();
	    }
    });

    $(rf_id('min') + ', ' + rf_id('max')).change(function(evt){
        fill_in_selection_in_summary();
    });

  }

 // TODO: This function needs a big re-write to decouple it from all submodules
this.update_filter_options = function(use_default){
    // TODO: Remove dependency on lc_id
    var data_set_id = $(lc_id('galaxy_model')).val();
    // fetch_data = update_filter_options.current_key != data_set_id;
    fetch_data = this.current_key != data_set_id;


    var isInt = function(value) {
        return !isNaN(parseInt(value)) && (parseFloat(value)+'' == parseInt(value)+'');
    }
    var isFloat = function(value) {
        return !isNaN(parseFloat(value));
    }

    function add_option($filter, item, current_filter) {
        $option = $('<option/>');
        $option.attr('value',item_to_value(item));
        if (item_to_value(item) == item_to_value(TAO_NO_FILTER)) {
            $option.html(item.fields.label);
        } else {
            if (item.fields.units != '') {
                $option.html(item.fields.label + ' (' + item.fields.units + ')');
            } else {
                $option.html(item.fields.label);
            }
        }
        if (item_to_value(item) == current_filter) {
            $option.attr('selected','selected');
        }
        $option.data('is_valid', item.fields.data_type==1? isFloat : isInt);
        $option.data('expected_type', item.fields.data_type==1? 'float' : 'integer');
        $filter.append($option);
    }

    function current_selection() {
        var list = [];
        $.each(catalogue.modules.light_cone.lc_output_props_widget.selected(), function(i,value) {
           list.push('D-' + value);
        });
        // TODO: Remove dependency
        if ($(sed_id('apply_sed')).is(':checked')) {
            $.each(catalogue.modules.sed.sed_band_pass_filters_widget.selected(), function(i,value) {
                list.push('B-' + value);
            });
        }
        return list;
    }

    function refresh_select(resp, use_default) {
        var $filter = $(rf_id('filter'));
        var current_filter = $filter.val();
        var current = current_selection();
        current.push(item_to_value(TAO_NO_FILTER));
        current.push('D-' + resp.default_id.toString());
        if (use_default || current.indexOf(current_filter) == -1) {
            current_filter = 'D-' + resp.default_id;
            if (current_filter == '' || current_filter == item_to_value(TAO_NO_FILTER)) {
                $(rf_id('min')).val('');
                $(rf_id('max')).val('');
            } else {
                $(rf_id('min')).val(resp.default_min);
                $(rf_id('max')).val(resp.default_max);
            }
        }
        $filter.empty();
        add_option($filter, TAO_NO_FILTER, current_filter);
        var data = resp.list;
        for(i=0; i<data.length; i++) {
            if (current.indexOf(item_to_value(data[i])) != -1) {
                add_option($filter, data[i], current_filter);
            }
        }
        $filter.change();
    }

    if (!fetch_data) {
        refresh_select(this.update_filter_options.current_data, use_default);
        return;
    }
    console.log('');
    $.ajax({
        url : TAO_JSON_CTX + 'filters/' + data_set_id,
        dataType: "json",
        error: function() {
            alert("Couldn't get filters");
        },
        success: function(resp, status, xhr) {
            me().update_filter_options.current_data = resp;
            me().update_filter_options.current_key = data_set_id;
            console.log([me().update_filter_options.output_props,
                me().update_filter_options.bandpass_props]);
            if (me().update_filter_options.output_props &&
                me().update_filter_options.bandpass_props) {
                refresh_select(resp, use_default);
            }
        }
    });
  };

  this.update_filter_options.initializing = true;
  this.update_filter_options.output_props = false;
  this.update_filter_options.bandpass_props = false;

  var validate_min_max = function() {

    var min = $(rf_id('min')).val();
    var max = $(rf_id('max')).val();
    var $filter = $(rf_id('filter'));
    if ($filter.val() == item_to_value(TAO_NO_FILTER)) { return true; }
    var $option = $filter.find('option:selected');
    var is_valid = $option.data('is_valid');
    var expected_type = $option.data('expected_type');
    var error = false;
    if (min && !is_valid(min)) {
        catalogue.util.show_error($(rf_id('min')),'Min in record filter should be ' + expected_type);
        error = true;
    } else {
        catalogue.util.show_error($(rf_id('min')), null);
    }
    if (max && !is_valid(max)) {
        catalogue.util.show_error($(rf_id('max')),'Max in record filter should be ' + expected_type);
        error = true;
    } else {
        catalogue.util.show_error($(rf_id('max')), null);
    }

    return !error;
}

  this.cleanup_fields = function($form) {

  }

  this.validate = function($form) {
  	return validate_min_max();
  }

  this.pre_submit = function($form) {
    $(lc_id('output_properties')+' option').each(function(i) {
        $(this).attr("selected", "selected");
    });
  }

  this.init = function() {
  	console.log('init record_filter module');
  	init_event_handlers();
  }

}



