/**
 * Created with PyCharm.
 * User: cindy
 * Date: 11/03/13
 * Time: 10:42 AM
 * To change this template use File | Settings | File Templates.
 */

$(function($){
    $('.openPopUp').each(function() {
        $.data(this, 'dialog',
            $(this).next('.popUpDialogue').dialog({
                autoOpen: false,
                modal: true,
                height: 435,
                width: 630,
                buttons: {
                    Ok: function() {
                        $(this).dialog("close");
                    }
                }
            })
        );
    }).click(function() {
        $.data(this, 'dialog').dialog('open');
        return false;
    });
});