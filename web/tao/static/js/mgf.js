var show_simulation_info;

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
})(jQuery);

jQuery(document).ready(function($) {

  var update_galaxy_options = (function(){
    var options_html = $('#id_dummy_galaxy_model').remove();
    options_html = '<select>' + options_html.html() + '</select>';
    $('#id_dummy_galaxy_model').remove();

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

  $('#id_dark_matter_simulation').change(function(evt){
    var $this = $(this);
    var sim_id = $this.val();

    show_simulation_info(sim_id);
    update_galaxy_options(sim_id);
  });

  (function(){
    var initial_simulation_id = $('#id_dark_matter_simulation').val();
    show_simulation_info(initial_simulation_id);
    update_galaxy_options(initial_simulation_id);
  })();
});
