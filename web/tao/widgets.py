"""
==================
tao.widgets
==================

Custom Django widgets
"""
from django import forms
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms.widgets import SelectMultiple, TextInput
from django.forms.util import flatatt
from django.utils.html import conditional_escape, escape, format_html, force_text
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


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
        if option_value is None and option_label is None:
            # Assume that we just want to supply the other attributes
            other_attrs_html = ' '.join('%s="%s"' % (escape(force_unicode(name)), escape(force_unicode(val))) for name, val in self.other_attrs[option_value].items())
            res = u'<option %s />' % other_attrs_html
        else:
            other_attrs_html = ' '.join('%s="%s"' % (escape(force_unicode(name)), escape(force_unicode(val))) for name, val in self.other_attrs[option_value].items())
            selected_html = u' selected="selected"' if (option_value in selected_choices) else ''
            option_label = conditional_escape(force_unicode(option_label))
            option_value = escape(force_unicode(option_value))
            res = u'<option value="%s"%s%s>%s</option>' % (option_value, other_attrs_html, selected_html, option_label)
        return res


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


class TwoSidedSelectWidget(SelectMultiple):
    class Media:
        js = ( static('js/TwoSidedSelectWidget.js'), )

    def __init__(self, attrs=None, choices=()):
        super(TwoSidedSelectWidget, self).__init__(attrs, choices)

    ## name and id are set by the framework
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        if 'ko_data' in self.attrs:
            data_bind = "value: %(value)s, template: {name: 'two_sided_select_widget', data: %(widget)s}" % self.attrs['ko_data']
            del self.attrs['ko_data']
            attrs['data-bind'] = data_bind
        final_attrs = self.build_attrs(attrs, id=name)
        output_right = [u'<div %s><select>' % flatatt(final_attrs)]
        options = self.render_options(choices, value)
        if options:
            output_right.append(options)
        output_right.append('</select></div>')
        resp = u'\n'.join(output_right)
        return mark_safe(resp)

class SpinnerWidget(TextInput):

    def __init__(self, attrs=None):
        super(SpinnerWidget, self).__init__(attrs)

    ## name and id are set by the framework
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        input_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        span_attrs = {}
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            input_attrs['value'] = force_text(self._format_value(value))
        if 'spinner_bind' in self.attrs:
            input_attrs['data-bind'] = self.attrs['spinner_bind']
            del input_attrs['spinner_bind']
        if 'spinner_message' in self.attrs:
            span_attrs['data-bind'] = self.attrs['spinner_message']
        input_part = '<input{0} />'.format(flatatt(input_attrs))
        span_part = '<span class="spinner-message" {0}></span>'.format(flatatt(span_attrs))
        return mark_safe('<div>' + input_part + '<br/>' + span_part +'</div>')

    def bind_label(self):
        return True


