"""
==================
tao.widgets
==================

Custom Django widgets
"""
from django import forms
from django.utils.html import conditional_escape, escape
from django.utils.encoding import force_unicode


# based on http://stackoverflow.com/questions/5089396/django-form-field-choices-adding-an-attribute
class SelectWithOtherAttrs(forms.Select):
    """
        Select widget accepting other attributes to be rendered in the options
            keyed on label
    """
    def __init__(self, *args, **kwargs):
        super(SelectWithOtherAttrs, self).__init__(*args, **kwargs)
        self.other_attrs = {}

    def render_option(self, selected_choices, option_value, option_label):
        other_attrs_html = ' '.join('%s="%s"' % (escape(force_unicode(name)), escape(force_unicode(val))) for name, val in self.other_attrs[option_value].items())
        option_value = escape(force_unicode(option_value))
        selected_html = u' selected="selected"' if (option_value in selected_choices) else ''
        option_label = conditional_escape(force_unicode(option_label))
        return u'<option value="%s"%s%s>%s</option>' % (option_value, other_attrs_html, selected_html, option_label)


class ChoiceFieldWithOtherAttrs(forms.ChoiceField):
    """
        Field that accepts custom HTML attrs per option
            e.g. ChoiceFieldWithOtherAttrs(choices=[(value, label, {'data-something': 'abc'}])
    """
    widget = SelectWithOtherAttrs

    def __init__(self, choices=(), *args, **kwargs):
        choice_pairs = [(c[0], c[1]) for c in choices]
        super(ChoiceFieldWithOtherAttrs, self).__init__(choices=choice_pairs, *args, **kwargs)
        self.widget.other_attrs = dict([(c[0], c[2]) for c in choices])
