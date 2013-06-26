$(function() {
    var moveLeft = 20;
    var moveDown = 10;

    $('a#trigger').hover(function() {
        $('div#why-register').show();
    }, function() {
        $('div#why-register').hide();
    });

//    $('a#trigger').mousemove(function(e) {
//        $('div#pop-up').css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
//    });
});
