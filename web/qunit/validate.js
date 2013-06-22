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

test("Disabled elements do not get checked.", function() {
    var called = false;
    var v1 = $('#id_select').validate().validate('test', {
        check: function(val) {
            called = true;
        },
        message: ''
    });
    $('#id_select').attr('disabled', 'disabled');
    ok(!called, "Must not be called.");
});

test("Select inputs have their value passed correctly.", function() {
    var v1 = $('#id_select').validate().validate('test', {
        check: function(val) {
            equal(val, "hello", "Must extract correct value.");
        },
        message: ''
    });
    $('#id_select').focus();
    $('#id_another').focus();
});

test("Required inputs have errors set.", function() {
    var v1 = $('#id_empty').validate({
        required: true
    }).validate('test', {
        check: function(val) {
            return true;
        },
        message: ''
    });
    $('#id_empty').focus();
    $('#id_another').focus();
    ok($('#id_empty').closest('.control-group').hasClass('error'), "Must have error set.");
});

test("Optional inputs do not have errors.", function() {
    var v1 = $('#id_empty').validate().validate('test', {
        check: function(val) {
            return true;
        },
        message: ''
    });
    $('#id_empty').focus();
    $('#id_another').focus();
    ok(!$('#id_empty').closest('.control-group').hasClass('error'), "Must not have error set.");
});

test("Checkbox values appear as boolean.", function() {
    var v1 = $('#id_check').validate().validate('test', {
        check: function(val) {
            ok(val === true || val === false, "Must be strictly true or false.");
            return true;
        },
        message: ''
    });
    $('#id_check').focus();
    $('#id_another').focus();
});

test("Validation always called if in error.", function() {
    var called = false;
    var v1 = $('#id_empty').validate().validate('test', {
        check: function(val) {
            called = true;
            return true;
        },
        message: ''
    });
    $.validate_all();
    ok(!called, 'Must not have called yet.')
    $('#id_empty').closest('.control-group').addClass('error');
    $.validate_all();
    ok(called, 'Must have called.');
});

test("No validation for empty fields.", function() {
    var called = false;
    var v1 = $('#id_empty').validate().validate('test', {
        check: function(val) {
            called = true;
            return true;
        },
        message: ''
    });
    $.validate_all();
    ok(!called, 'Must not have called.')
});

function module_teardown() {
    $('#id_something').removeData();
    $('#id_something').unbind('focusout')
    $('#id_another').removeData();
    $('#id_another').unbind('focusout')
    $('#id_select').removeData();
    $('#id_select').unbind('focusout')
    $('#id_select').removeAttr('disabled');
    $('#id_empty').closest('.control-group').removeClass('error');
    $('#id_empty').removeData();
    $('#id_empty').unbind('focusout')
    $('#id_check').removeData();
    $('#id_check').unbind('focusout')
}
