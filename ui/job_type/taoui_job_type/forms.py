"""
========================
taoui_job_type.forms
========================
"""
from django import forms
from django.utils.translation import ugettext_lazy as _

from form_utils.forms import BetterForm
import form_utils.fields as bf_fields

from tao import datasets
from tao import models as tao_models
from tao.forms import FormsGraph
from tao.widgets import ChoiceFieldWithOtherAttrs, SelectWithOtherAttrs, TwoSidedSelectWidget
from tao.xml_util import module_xpath, module_xpath_iterate


####

class Form(BetterForm):
    EDIT_TEMPLATE = 'taoui_job_type/edit.html'
    MODULE_VERSION = 1
    SUMMARY_TEMPLATE = 'taoui_job_type/summary.html'
    LABEL = 'Job Type'


    def __init__(self, *args, **kwargs):
        self.ui_holder = args[0]
        super(Form, self).__init__(*args[1:], **kwargs)

        self.fields['params_file'] = forms.FileField(required=False, label='', widget=forms.FileInput(attrs={'form': 'file_upload'}))

    @classmethod
    def from_xml(cls, ui_holder, xml_root, prefix=None):
        return cls(ui_holder, {}, prefix=prefix)

    # Empty implementation to conform to module interface
    def to_xml(self, root):
        pass