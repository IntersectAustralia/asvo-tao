module('validator', {
    teardown: module_teardown
});

test("Empty constructor.", function() {
    var v1 = $('#id_something').validate();
    var data = v1.data('validate');
    ok(data.type === undefined, "Type must be undefined.");
    ok(data.form === undefined, "Form must be undefined.");
});

test("No elements to construct", 0, function() {
    $('#nothing').validate();
});

test("Construct with cache.", function() {
    var the_cache = {
        one: 'one',
        two: 'two'
    }
    var v1 = $('#id_something').validate({
        cache: the_cache
    });
    var data = v1.data('validate');
    deepEqual(data.cache, the_cache, 'Must have set cache.');
});

test("Construct with form.", function() {
    var v1 = $('#id_something').validate({
        form: 'hello'
    });
    var data = v1.data('validate');
    equal(data.form, 'hello', 'Must have set form.');
});

test("Construct with group.", function() {
    var v1 = $('#id_something').validate({
        group: [$('#id_another'), $('#id_more')]
    });
    var data = v1.data('validate');
    deepEqual(data.group, [$('#id_another'), $('#id_more')], 'Must have set group.');
});

test("Add test.", function() {
    function the_check() {
    }
    var the_message = 'the message';
    var v1 = $('#id_something').validate().validate('test', {
        check: the_check,
        message: the_message
    });
    var data = v1.data('validate');
    equal(data.tests.length, 1, 'Must be one test created.');
    equal(data.tests[0][0], the_check, 'Must have set the check.');
    equal(data.tests[0][1], the_message, 'Must have set the message.');
});

test("Call sequential passing tests.", function() {
    var called_one = false, called_two = false;
    function check_one() {
        called_one = true;
        return true;
    }
    function check_two() {
        called_two = true;
        return true;
    }
    var v1 = $('#id_something').validate().validate('test', {
        check: check_one,
        message: ''
    }).validate('test', {
        check: check_two,
        message: ''
    });
    $('#id_something').focus();
    $('#id_another').focus();
    var data = v1.data('validate');
    ok(called_one && called_two, 'Must have called both tests.');
});

test("Call sequential failing tests.", function() {
    var called_one = false, called_two = false;
    function check_one() {
        called_one = true;
        return false;
    }
    function check_two() {
        called_two = true;
        return false;
    }
    var v1 = $('#id_something').validate().validate('test', {
        check: check_one,
        message: ''
    }).validate('test', {
        check: check_two,
        message: ''
    });
    $('#id_something').focus();
    $('#id_another').focus();
    var data = v1.data('validate');
    ok(called_one, 'Must have called first test.');
    ok(!called_two, 'Must not have called second test.');
});

test("Tests recieve cache.", function() {
    var v1 = $('#id_something').validate({
        cache: {
            another: $('#id_another')
        }
    }).validate('test', {
        check: function(val, cache) {
            equal(cache.another, 'two');
        },
        message: ''
    });
    $('#id_something').focus();
    $('#id_another').focus();
});

test("Failed tests modify class.", function() {
    var v1 = $('#id_something').validate().validate('test', {
        check: function() {
            return false;
        },
        message: ''
    });
    $('#id_something').focus();
    $('#id_another').focus();
    ok($('#id_something').closest('.control-group').hasClass('error'), 'Must set error class.');
});

test("Successful tests do not modify class.", function() {
    var v1 = $('#id_something').validate().validate('test', {
        check: function() {
            return true;
        },
        message: ''
    });
    $('#id_something').focus();
    $('#id_another').focus();
    ok(!$('#id_something').closest('.control-group').hasClass('error'), 'Must not set error class.');
});

test("Group members are checked first.", function() {
    var called_something = false, called_another = false;
    var v1 = $('#id_another').validate({
        group: [$('#id_something')]
    }).validate('test', {
        check: function() {
            called_another = true;
            return true;
        },
        message: ''
    });
    var v2 = $('#id_something').validate({
        group: [$('#id_another')]
    }).validate('test', {
        check: function() {
            called_something = true;
            return true;
        },
        message: ''
    });
    $('#id_something').focus();
    $('#id_another').focus();
    ok(called_another && called_something, 'Must have called both inputs.');
});

test("Validating forms call all inputs.", function() {
    var called_something = false, called_another = false;
    var v1 = $('#id_something').validate({
        form: 'the_form'
    }).validate('test', {
        check: function() {
            called_something = true;
            return true;
        },
        message: ''
    });
    var v2 = $('#id_another').validate({
        form: 'the_form'
    }).validate('test', {
        check: function() {
            called_another = true;
            return true;
        },
        message: ''
    });
    $.validate_form('the_form');
    ok(called_another && called_something, 'Must have called both inputs.');
});

test("Removing from DOM removes from forms.", function() {
    var called = false;
    var v1 = $('#id_something').validate({
        form: 'the_form'
    }).validate('test', {
        check: function() {
            called = true;
            return true;
        },
        message: ''
    });
    $('#id_something').remove();
    v1.remove();
    $.validate_form('the_form');
    ok(!called, 'Must not call the test.');
});

function module_teardown() {
    $('#id_something').removeData();
    $('#id_something').unbind('focusout')
    $('#id_another').removeData();
    $('#id_another').unbind('focusout')
}
