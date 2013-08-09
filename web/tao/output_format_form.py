from django import forms

from form_utils.forms import BetterForm

import tao.settings as tao_settings
from tao.forms import FormsGraph
from tao.xml_util import module_xpath

from tao.widgets import ChoiceFieldWithOtherAttrs, SelectWithOtherAttrs

#### XML version 2 ####

def to_xml_2(form, root):
   from tao.xml_util import find_or_create, child_element

   # Hunt down the full item from the list of output formats.
   fmt = form.cleaned_data['supported_formats']
   ext = ''
   for x in tao_settings.OUTPUT_FORMATS:
       if x['value'] == fmt:
           ext = '.' + x['extension']
           break

   # The output file should be a CSV, by default.
   of_elem = find_or_create(root, fmt, id=FormsGraph.OUTPUT_ID)
   child_element(of_elem, 'module-version', text=OutputFormatForm.MODULE_VERSION)
   child_element(of_elem, 'filename', text='tao.output' + ext)

def from_xml_2(cls, ui_holder, xml_root, prefix=None):
    params = {prefix+'-supported_formats': 'csv'}
    for fmt in tao_settings.OUTPUT_FORMATS:
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

    class Meta:
        fieldsets = [('primary', {
            'legend': '',
            'fields': ['supported_formats']
        }),]

    def __init__(self, *args, **kwargs):
        super(OutputFormatForm, self).__init__(*args[1:], **kwargs)
        self.fields['supported_formats'] = ChoiceFieldWithOtherAttrs(required=False,
                                    label='Output Format',
                                    choices=[(None, None, {"data-bind" : "value: $data, text: $data.fields.text"})],
                                    widget=SelectWithOtherAttrs(attrs={'class': 'light_box_field'}))
        self.fields['supported_formats'].widget.attrs['data-bind'] = 'foreach: output_formats, value: output_format'


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

