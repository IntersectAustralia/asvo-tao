jQuery(document).ready(function($) {
  var options_html = $('#id_dummy_galaxy_model').remove();
  options_html = '<select>' + options_html.html() + '</select>';
  $('#id_dummy_galaxy_model').remove();

  $('#id_dark_matter_simulation').change(function(evt){
    var $this = $(this);
    var sim_id = $this.val();
    var $applicable_options = $(options_html);
    $applicable_options.find('option').each(function(){
      if ($(this).attr('data-sim') != sim_id) {
        $(this).remove();
      }
    });
    $('#id_galaxy_model').html($applicable_options.html());
  });
});
