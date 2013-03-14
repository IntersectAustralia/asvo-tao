/**
 * Created with PyCharm.
 * User: cindy
 * Date: 11/03/13
 * Time: 10:42 AM
 * To change this template use File | Settings | File Templates.
 */

$(function(){

    $('#popUpDialogue').dialog({
        autoOpen: false,
        modal: true,
        height: 435,
        width: 630,
        buttons: {
            Ok: function() {
                $(this).dialog("close");
            }
        }
    });

    $('#popUp').click(function(e) {
        $('#popUpDialogue').dialog("open");
    });
});