from django import forms

from form_utils.forms import BetterForm

import tao.settings as tao_settings
from tao.forms import FormsGraph
from tao.xml_util import module_xpath

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
   of_elem = find_or_create(root, fmt+'-dump', id=FormsGraph.OUTPUT_ID)
   child_element(of_elem, 'module-version', text=OutputFormatForm.MODULE_VERSION)
   child_element(of_elem, 'filename', text='tao.output' + ext)

def from_xml_2(cls, ui_holder, xml_root, prefix=None):
   supported_format = 'csv'
   return cls(ui_holder, {prefix + '-supported_formats': supported_format}, prefix=prefix)

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
        self.fields['supported_formats'] = forms.ChoiceField(choices=[(x['value'], x['text']) for x in tao_settings.OUTPUT_FORMATS])

    def to_xml(self, parent_xml_element):
        version = 2.0
        to_xml_2(self, parent_xml_element)

    @classmethod
    def from_xml(cls, ui_holder, xml_root, prefix=None):
        version = module_xpath(xml_root, '//workflow/schema-version')
        if version == '2.0':
            return from_xml_2(cls, ui_holder, xml_root, prefix=prefix)
