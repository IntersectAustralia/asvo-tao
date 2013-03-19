/**
 * Created with PyCharm.
 * User: cindy
 * Date: 18/03/13
 * Time: 3:58 PM
 * To change this template use File | Settings | File Templates.
 */

$(function() {

    $("#id_light_cone-number_of_light_cones").spinner({
        spin: function( event, ui ) {
            if ( ui.value > 10 ) {
                $(this).spinner("value",10);
                return false;
            } else if ( ui.value < 0 ) {
                $(this).spinner("value", 0);
                return false;
            }
        }
    });
});