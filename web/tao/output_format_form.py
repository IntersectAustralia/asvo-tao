from django import forms

from form_utils.forms import BetterForm

import tao.settings as tao_settings
from django.conf import settings
from tao.forms import FormsGraph
from tao.xml_util import module_xpath
from tao.models import GlobalParameter

from tao.widgets import ChoiceFieldWithOtherAttrs, SelectWithOtherAttrs

#### XML version 2 ####

def configured_output_formats():
    "Answer the list of output formats from GlobalParameter output_formats"
    return eval(GlobalParameter.objects.get(parameter_name='output_formats').parameter_value.replace('\r',''))

def to_xml_2(form, root):
   from tao.xml_util import find_or_create, child_element

   # Hunt down the full item from the list of output formats.
   fmt = form.cleaned_data['supported_formats']
   ext = ''
   for x in configured_output_formats():
       if x['value'] == fmt:
           ext = '.' + x['extension']
           break

   # The output file should be a CSV, by default.
   of_elem = find_or_create(root, fmt, id=FormsGraph.OUTPUT_ID)
   child_element(of_elem, 'module-version', text=OutputFormatForm.MODULE_VERSION)
   child_element(of_elem, 'filename', text='tao.output' + ext)

def from_xml_2(cls, ui_holder, xml_root, prefix=None):
    params = {prefix+'-supported_formats': 'csv'}
    for fmt in configured_output_formats():
        supported_format = module_xpath(xml_root, '//' + fmt['value'], text=False)
        if supported_format is not None:
            params.update({prefix+'-supported_formats': fmt['value']})
    return cls(ui_holder, params, prefix=prefix)

########################


class OutputFormatForm(BetterForm):
    EDIT_TEMPLATE = 'mock_galaxy_factory/output_format.html'
    MODULE_VERSION = 1
    SUMMARY_TEMPLATE = 'mock_galaxy_factory/output_format_summary.html'
    LABEL = 'Output format'
    TAB_ID = settings.MODULE_INDICES['output_format']

    class Meta:
        fieldsets = [('primary', {
            'legend': '',
            'fields': ['supported_formats']
        }),]

    def __init__(self, *args, **kwargs):
        super(OutputFormatForm, self).__init__(*args[1:], **kwargs)
        if self.is_bound:
            format_choices = [(x['value'], x['text'], {}) for x in configured_output_formats()]
        else:
            format_choices = [(None, None, {"data-bind" : "value: $data, text: $data.fields.text"})]
        self.fields['supported_formats'] = ChoiceFieldWithOtherAttrs(required=False,
                                    label='Output Format',
                                    choices=format_choices,
                                    widget=SelectWithOtherAttrs(attrs={'class': 'light_box_field'}))
        self.fields['supported_formats'].widget.attrs['data-bind'] = 'foreach: output_formats, value: output_format'


    def to_json_dict(self):
        """Answer the json dictionary representation of the receiver.
        i.e. something that can easily be passed to json.dumps()"""
        json_dict = {}
        for fn in self.fields.keys():
            ffn = self.prefix + '-' + fn
            val = self.data.get(ffn)
            if val is not None:
                json_dict[ffn] = val
        return json_dict

    def to_xml(self, parent_xml_element):
        version = 2.0
        to_xml_2(self, parent_xml_element)

    @classmethod
    def from_xml(cls, ui_holder, xml_root, prefix=None):
        version = module_xpath(xml_root, '//workflow/schema-version')
        if version == '2.0':
            return from_xml_2(cls, ui_holder, xml_root, prefix=prefix)
        else:
            return cls(ui_holder, {}, prefix=prefix)

