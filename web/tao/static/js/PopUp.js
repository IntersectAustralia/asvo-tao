$(function() {
    $('a#show-why-register').click(function(e) {
        e.stopPropagation();
        $('div#why-register').show();
        return false;
    });

    $("a#close-why-register").click(function() {
        $('div#why-register').hide();
        return false;
    });
});
