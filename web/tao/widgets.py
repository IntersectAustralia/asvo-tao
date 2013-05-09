"""
==================
tao.widgets
==================

Custom Django widgets
"""
from django import forms
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms.widgets import SelectMultiple
from django.forms.util import flatatt
from django.utils.html import conditional_escape, escape
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


class TwoSidedSelectWidget(SelectMultiple):
    class Media:
        js = ( static('js/TwoSidedSelectWidget.js'), )

    def __init__(self, attrs=None, choices=()):
        super(TwoSidedSelectWidget, self).__init__(attrs, choices)

    ## name and id are set by the framework
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, name=name)
        widget_id = final_attrs['id']
        left_attrs = {'id': widget_id+'_from'}
        filter_attrs = {'id': widget_id+'_filter'}
        output_filter = [u'<input type="text" placeholder="Filter" %s>' % flatatt(filter_attrs)]
        output_left = [u'<select multiple="multiple"%s>' % flatatt(left_attrs), u'</select>',
                       ]
        output_right = [u'<select multiple="multiple"%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, value)
        if options:
            output_right.append(options)
        output_right.append('</select>')
        output = [u'<table id="' + widget_id + '-table"><tr>']
        output.extend(['<td id="' + widget_id + '-left"><i>Available</i><br/>'] + output_filter + ['<br/>'] + output_left + ['</td>'])
        output.extend(['<td class="text-align:center;">',
                       u'<a href="#" id="%s_op_add_all" style="display:block;text-decoration:none;clear:both;">&gt;&gt;</a>' % widget_id,
                       u'<a href="#" id="%s_op_add" style="display:block;text-decoration:none;clear:both;">&gt;</a>' % widget_id,
                       u'<a href="#" id="%s_op_remove" style="display:block;text-decoration:none;clear:both;">&lt;</a>' % widget_id,
                       u'<a href="#" id="%s_op_remove_all" style="display:block;text-decoration:none;clear:both;">&lt;&lt;</a>' % widget_id,
                       '</td>'])
        output.extend(['<td id="' + widget_id + '-right"><i>Selected</i><br/>'] + output_right + ['</td>'])
        output.extend([u'</tr></table>'])
        return mark_safe(u'\n'.join(output))
