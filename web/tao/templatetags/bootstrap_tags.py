from django.template import Context
from django.template.loader import get_template
from django import template
from django.forms.fields import CheckboxInput

register = template.Library()


@register.filter
def as_bootstrap(form):
    template = get_template('bootstrap/form.html')
    ctx = Context({'form': form})
    return template.render(ctx)


@register.filter
def as_bootstrap_field(field):
    template = get_template('bootstrap/field.html')
    ctx = Context({'field': field})
    return template.render(ctx)


@register.filter
def as_bootstrap_fieldset(fieldset):
    template = get_template('bootstrap/fieldset.html')
    ctx = Context({'fieldset': fieldset})
    return template.render(ctx)


@register.filter(name='is_checkbox')
def is_checkbox(value):
    return isinstance(value, CheckboxInput)

@register.assignment_tag
def check_user(user, method):
    try:
        m = getattr(user,method)
        if callable(m):
            if m():
                return True
            else:
                return False
        else:
            return False
    except AttributeError:
        return False
