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
from tao.forms import FormsGraph
from tao.widgets import ChoiceFieldWithOtherAttrs, TwoSidedSelectWidget
from tao.xml_util import module_xpath, module_xpath_iterate

#### XML version 2 ####

def to_xml_2(form, root):
    apply_sed = form.cleaned_data.get('apply_sed')
    output_format = form.ui_holder.cleaned_data('output_format', 'supported_formats')

    if apply_sed:
        from tao.xml_util import find_or_create, child_element

        sed_elem = find_or_create(root, 'sed', id=FormsGraph.SED_ID)
        child_element(sed_elem, 'module-version', text=Form.MODULE_VERSION)

        # Add a hard-coded connection to the light-cone and the CSV output.
        child_element(child_element(sed_elem, 'parents'), 'item', text=FormsGraph.LIGHT_CONE_ID)

        child_element(child_element(find_or_create(root, output_format, id=FormsGraph.OUTPUT_ID), 'parents'), 'item', text=FormsGraph.BANDPASS_FILTER_ID)

        single_stellar_population_model = tao_models.StellarModel.objects.get(pk=form.cleaned_data['single_stellar_population_model'])
        child_element(sed_elem, 'single-stellar-population-model', text=single_stellar_population_model.name)

        # Create an independant filter module.
        filter_elem = find_or_create(root, 'filter', id=FormsGraph.BANDPASS_FILTER_ID)
        child_element(filter_elem, 'module-version', text=Form.MODULE_VERSION)

        apply_dust = form.cleaned_data['apply_dust']
        if apply_dust:
            dust_elem = find_or_create(root, 'dust', id=FormsGraph.DUST_ID)
            child_element(dust_elem, 'module-version', text=Form.MODULE_VERSION)
            child_element(child_element(dust_elem, 'parents'), 'item', text=FormsGraph.SED_ID)
            selected_dust_model = tao_models.DustModel.objects.get(pk=form.cleaned_data['select_dust_model'])
            child_element(dust_elem, 'model', text=selected_dust_model.name)
            # Parent of the dust module is either the SED module or, if selected, the dust module
            child_element(child_element(filter_elem, 'parents'), 'item', text=FormsGraph.DUST_ID)
        else:
            child_element(child_element(filter_elem, 'parents'), 'item', text=FormsGraph.SED_ID)

        # Find the CSV output element or create it, and get access to
        # the fields tag.
        fields_elem = find_or_create(find_or_create(root, output_format, id=FormsGraph.OUTPUT_ID), 'fields')

        band_pass_filters = form.cleaned_data['band_pass_filters']
        if len(band_pass_filters) > 0:
            bf_elem = child_element(filter_elem, 'bandpass-filters')
            added = {}
            selected = {}
            for item in band_pass_filters:
                item_id, item_extension = item.split('_')
                if item_id not in selected: selected[item_id] = []
                selected[item_id].append(item_extension)
            for item in band_pass_filters:
                item_id, item_extension = item.split('_')
                op = datasets.band_pass_filter(item_id)
                if item_id not in added:
                    child_element(bf_elem, 'item', text=op.filter_id, label=op.label, description=op.description, selected=",".join(selected[item_id]))
                    added[item_id] = True
                child_element(fields_elem, 'item', text=op.filter_id + '_' + item_extension, label=op.label + ' (' + item_extension.capitalize() + ')')

    else:
        from tao.xml_util import find_or_create, child_element

        # No SED module, connect the output to the light-cone module.
        child_element(child_element(find_or_create(root, output_format, id=FormsGraph.OUTPUT_ID), 'parents'), 'item', text=FormsGraph.LIGHT_CONE_ID)

def from_xml_2(cls, ui_holder, xml_root, prefix=None):
    sed = module_xpath(xml_root, '//workflow/sed', text=False)
    apply_sed = sed is not None
    params = {prefix+'-apply_sed': apply_sed}
    if apply_sed:
        sspm_name = module_xpath(xml_root, '//sed/single-stellar-population-model')
        sspm = datasets.stellar_model_find_from_xml(sspm_name)
        if sspm is not None:
            params.update({prefix+'-single_stellar_population_model': sspm.id})
        bp_filters = []
        for filter_item in module_xpath_iterate(xml_root, '//filter/bandpass-filters/item', text=False):
            filter_id = filter_item.text
            filter_extension_list = filter_item.get('selected').split(',')
            filter = datasets.band_pass_filter_find_from_xml(filter_id)
            if filter is not None:
                for filter_extension in filter_extension_list:
                    bp_filters.append(str(filter.id) + '_' + filter_extension)
        if len(bp_filters) > 0:
            params.update({prefix+'-band_pass_filters': bp_filters})
        dust = module_xpath(xml_root, '//dust/model')
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

#######################


class Form(BetterForm):
    EDIT_TEMPLATE = 'taoui_sed/edit.html'
    MODULE_VERSION = 1
    SUMMARY_TEMPLATE = 'taoui_sed/summary.html'
    LABEL = 'Spectral Energy Distribution'

    SED_REQUIRED_FIELDS = ('single_stellar_population_model', 'band_pass_filters')

    class Meta:
        fieldsets = [
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
        if self.is_bound:
            sspm_choices = datasets.stellar_model_choices()
            dust_models = [(x.id, x.label) for x in datasets.dust_models_objects()]
        else:
            sspm_choices = []
            dust_models = []

        self.fields['apply_sed'] = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label='Apply Spectral Energy Distribution')
        self.fields['single_stellar_population_model'] = ChoiceFieldWithOtherAttrs(choices=sspm_choices, required=default_required)
        self.fields['band_pass_filters'] = bf_fields.forms.MultipleChoiceField(required=default_required,
                                choices=datasets.band_pass_filters_enriched(),
                                widget=TwoSidedSelectWidget)
        self.fields['apply_dust'] = forms.BooleanField(required=default_required, widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), label='Apply Dust')
        self.fields['select_dust_model'] = forms.ChoiceField(choices=dust_models, required=default_required, widget=forms.Select())

        for field_name in Form.SED_REQUIRED_FIELDS:
            self.fields[field_name].semirequired = True

        self.fields['apply_sed'].widget.attrs['data-bind'] = 'checked: apply_sed'
        self.fields['single_stellar_population_model'].widget.attrs['data-bind'] = 'options: stellar_models, value: stellar_model, optionsText: function(i) { return i.fields.label }'
        self.fields['band_pass_filters'].widget.attrs['ko_data'] = 'bandpass_filters'
        self.fields['band_pass_filters'].widget.attrs['data-bind'] = 'value: bandpass_filters'
        self.fields['apply_dust'].widget.attrs['data-bind'] = 'checked: apply_dust'
        self.fields['select_dust_model'].widget.attrs['data-bind'] = 'options: dust_models, value: dust_model, optionsText: function(i) { return i.fields.label }'

    def get_apply_sed(self):
        # use this to ensure a BoundField is returned
        return self['apply_sed']

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

    def to_json_dict(self):
        """Answer the json dictionary representation of the receiver.
        i.e. something that can easily be passed to json.dumps()"""
        json_dict = {}
        ffn = self.prefix + '-apply_sed'
        apply_sed = self.data[ffn]
        json_dict[ffn] = apply_sed
        if apply_sed:
            for fn in ['single_stellar_population_model', 'apply_dust',
                       'select_dust_model']:
                ffn = self.prefix + '-' + fn
                val = self.data.get(ffn)
                if val is not None:
                    json_dict[ffn] = val
        return json_dict


    def to_xml(self, root):
        version = 2.0
        to_xml_2(self, root)

    @classmethod
    def from_xml(cls, ui_holder, xml_root, prefix=None):
        version = module_xpath(xml_root, '//workflow/schema-version')
        if version == '2.0':
            return from_xml_2(cls, ui_holder, xml_root, prefix=prefix)
        else:
            return cls(ui_holder, {}, prefix=prefix)

