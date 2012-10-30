var show_simulation_info;
var show_galaxy_model_info;

(function($){
	show_simulation_info = function(simulation_id) {
	  $('div.simulation-info').each(function() {
		  var $sim_div = $(this);
		  if ($sim_div.attr('data-simulation_id') === simulation_id) {
			  $sim_div.show();
		  } else {
			  $sim_div.hide();
		  }
	  });
	};
	show_galaxy_model_info = function(galaxy_model_id) {
	  $('div.galaxy-model-info').each(function() {
		  var $galaxy_model_div = $(this);
		  if ($galaxy_model_div.attr('data-galaxy-model-id') === galaxy_model_id) {
			  $galaxy_model_div.show();
		  } else {
			  $galaxy_model_div.hide();
		  }
	  });
	};
})(jQuery);

jQuery(document).ready(function($) {

  var update_galaxy_options = (function(){
    var options_html = $('#id_galaxy_model');
    options_html = '<select>' + options_html.html() + '</select>';

    return function(simulation_id) {
      var $applicable_options = $(options_html);
      $applicable_options.find('option').each(function(){
        var $option = $(this);
        if ($option.attr('data-simulation_id') != simulation_id) {
          $option.remove();
        }
      });
      $('#id_galaxy_model').html($applicable_options.html());
    };
  })();

  var update_filter_options = (function(){
	var options_html = $('#id_filter');
	options_html = '<select>' + options_html.html() + '</select>';
	
	return function(simulation_id, galaxy_model_id) {
		var $applicable_options = $(options_html);
		$applicable_options.find('option').each(function(){
			var $option = $(this);
			if ($option.attr('value') != "no_filter" &&
				($option.attr('data-simulation_id') != simulation_id || $option.attr('data-galaxy_model_id') != galaxy_model_id)) {
				$option.remove();
			}
		});
		$('#id_filter').html($applicable_options.html());
	};
  })();
  
  $('#id_dark_matter_simulation').change(function(evt){
    var $this = $(this);
    var sim_id = $this.val();

    show_simulation_info(sim_id);
    update_galaxy_options(sim_id);
    $('#id_galaxy_model').change();
  });
  
  $('#id_galaxy_model').change(function(evt){
	  var $this = $(this);
	  var galaxy_model_id = $this.val();
	  
	  show_galaxy_model_info(galaxy_model_id);
	  
	  var simulation_id = $this.find('option').attr('data-simulation_id');
	  update_filter_options(simulation_id, galaxy_model_id);
  });
  
  $('#id_filter').change(function(evt){
	  var $this = $(this);
	  var filter_value = $this.val();
	  
	  if (filter_value == "no_filter") {
		  $('#id_max').attr('disabled', 'disabled');
		  $('#id_min').attr('disabled', 'disabled')
	  } else {
		  $('#id_max').removeAttr('disabled');
		  $('#id_min').removeAttr('disabled');
	  }
  });
  
  (function(){
    var initial_simulation_id = $('#id_dark_matter_simulation').val();
    show_simulation_info(initial_simulation_id);
    update_galaxy_options(initial_simulation_id);
    var initial_galaxy_model_id = $('#id_galaxy_model').val();
    show_galaxy_model_info(initial_galaxy_model_id);
    update_filter_options(initial_simulation_id, initial_galaxy_model_id);
    $('#id_filter').change();
  })();
});
