"""
========================
taoui_sed.forms
========================

"""

import os

from django import forms
import form_utils.fields as bf_fields
from form_utils.forms import BetterForm

from tao import datasets
from tao import models as tao_models
from tao.widgets import ChoiceFieldWithOtherAttrs, TwoSidedSelectWidget
from tao.xml_util import module_xpath, module_xpath_iterate


class Form(BetterForm):
    EDIT_TEMPLATE = 'taoui_sed/edit.html'
    MODULE_VERSION = 1
    SUMMARY_TEMPLATE = 'taoui_sed/summary.html'
    LABEL = 'Spectral Energy Distribution'

    SED_REQUIRED_FIELDS = ('single_stellar_population_model', 'band_pass_filters')

    class Meta:
        fieldsets = [
            ('topmost', {
                'legend': '',
                'fields': ['apply_sed'],
            }),
            ('primary', {
                'legend': 'Model',
                'fields': ['single_stellar_population_model',],
            }),
            ('secondary', {
                'legend': 'Output Band Pass Filters',
                'fields': ['band_pass_filters'],
            }),
            ('tertiary', {
                'legend': 'Dust Filter',
                'fields': ['apply_dust', 'select_dust_model'],
            }),
        ]

    def __init__(self, *args, **kwargs):
        self.ui_holder = args[0]
        super(Form, self).__init__(*args[1:], **kwargs)

        default_required = False
        objs = datasets.band_pass_filters_objects()
        bandpass_filters = [(x.id, x.label) for x in objs]
        dust_models = [(x.id, x.label) for x in datasets.dust_models_objects()]

        self.fields['apply_sed'] = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label='Apply Spectral Energy Distribution')
        self.fields['single_stellar_population_model'] = ChoiceFieldWithOtherAttrs(choices=datasets.stellar_model_choices(), required=default_required)
        self.fields['band_pass_filters'] = bf_fields.forms.MultipleChoiceField(required=default_required, choices=bandpass_filters, widget=TwoSidedSelectWidget)
        self.fields['apply_dust'] = forms.BooleanField(required=default_required, widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), label='Apply Dust')
        self.fields['select_dust_model'] = forms.ChoiceField(choices=dust_models, required=default_required, widget=forms.Select())

        for field_name in Form.SED_REQUIRED_FIELDS:
            self.fields[field_name].semirequired = True

    def check_sed_required_fields(self):
        apply_sed = self.cleaned_data.get('apply_sed')

        if apply_sed:
            for field_name in self.SED_REQUIRED_FIELDS:
                field = self.cleaned_data.get(field_name)
                if (field is None or field == '' or len(field) == 0) and field_name not in self._errors:
                    self.errors[field_name] = self.error_class(['This field is required.'])

    def check_dust_required_fields(self):
        apply_sed = self.cleaned_data.get('apply_sed')
        apply_dust = self.cleaned_data.get('apply_dust')

        if apply_sed and apply_dust:
            dust_model = self.cleaned_data.get('select_dust_model')
            if (dust_model is None or dust_model == '') and 'select_dust_model' not in self._errors:
                self.errors['select_dust_model'] = self.error_class(['This field is required.'])

    def clean(self):
        self.check_sed_required_fields()
        self.check_dust_required_fields()
        return self.cleaned_data

    def to_xml(self, root):
        apply_sed = self.cleaned_data.get('apply_sed')

        if apply_sed:
            from tao.xml_util import find_or_create, child_element

            sed_elem = find_or_create(root, 'sed', module='sed')

            # Add a hard-coded connection to the light-cone and the CSV output.
            child_element(child_element(sed_elem, 'parents'), 'item', text='light-cone')
            child_element(child_element(find_or_create(root, 'csv', module='csv'), 'parents'), 'item', text='filter')

            single_stellar_population_model = tao_models.StellarModel.objects.get(pk=self.cleaned_data['single_stellar_population_model'])

            child_element(sed_elem, 'module-version', text=Form.MODULE_VERSION)
            child_element(sed_elem, 'single-stellar-population-model', text=single_stellar_population_model.name)

            apply_dust = self.cleaned_data['apply_dust']
            if apply_dust:
                selected_dust_model = tao_models.DustModel.objects.get(pk=self.cleaned_data['select_dust_model'])
                child_element(sed_elem, 'dust', text=selected_dust_model.name)

            # Create an independant filter module.
            filter_elem = find_or_create(root, 'filter', module='filter')

            # Add a hard-coded connection to the SED module.
            child_element(child_element(filter_elem, 'parents'), 'item', text='sed')

            # Find the CSV output element or create it, and get access to
            # the fields tag.
            fields_elem = find_or_create(find_or_create(root, 'csv', module='csv'), 'fields')

            band_pass_filters = self.cleaned_data['band_pass_filters']
            if len(band_pass_filters) > 0:
                bf_elem = child_element(filter_elem, 'bandpass-filters')
                for item in band_pass_filters:
                    op = datasets.band_pass_filter(item)
                    child_element(bf_elem, 'item', text=op.filter_id, label=op.label)
                    bpf = os.path.splitext(op.filter_id)[0]
                    child_element(fields_elem, 'item', text=bpf + '_absolute', label=op.label)
                    child_element(fields_elem, 'item', text=bpf + '_apparent', label=op.label)

        else:
            from tao.xml_util import find_or_create, child_element

            # No SED module, connect the output to the light-cone module.
            child_element(child_element(find_or_create(root, 'csv', module='csv'), 'parents'), 'item', text='light-cone')

    @classmethod
    def from_xml(cls, ui_holder, xml_root, prefix=None):
        sed = module_xpath(xml_root, '//workflow/sed', text=False)
        apply_sed = sed is not None
        params = {prefix+'-apply_sed': apply_sed}
        if apply_sed:
            sspm_name = module_xpath(xml_root, '//sed/single-stellar-population-model')
            sspm = datasets.stellar_model_find_from_xml(sspm_name)
            if sspm is not None:
                params.update({prefix+'-single_stellar_population_model': sspm.id})
            bp_filters = []
            for filter_id in module_xpath_iterate(xml_root, '//filter/bandpass-filters/item'):
                filter = datasets.band_pass_filter_find_from_xml(filter_id)
                if filter is not None: bp_filters.append(filter.id)
            if len(bp_filters) > 0:
                params.update({prefix+'-band_pass_filters': bp_filters})
            dust = module_xpath(xml_root, '//sed/dust')
            apply_dust = dust is not None
            if apply_dust:
                dust_model = datasets.dust_model_find_from_xml(dust)
                if dust_model is not None:
                    params.update({prefix+'-apply_dust': True})
                    params.update({prefix+'-select_dust_model': dust_model.id})
                else:
                    params.update({prefix+'-apply_dust': False})
            else:
                params.update({prefix+'-apply_dust': False})
        return cls(ui_holder, params, prefix=prefix)
