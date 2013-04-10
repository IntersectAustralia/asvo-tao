"""
========================
taoui_light_cone.forms
========================
"""
from django import forms
from django.utils.translation import ugettext_lazy as _

from form_utils.forms import BetterForm
import form_utils.fields as bf_fields

from tao import datasets
from tao import models as tao_models
from tao.widgets import ChoiceFieldWithOtherAttrs, SelectWithOtherAttrs, TwoSidedSelectWidget
from tao.xml_util import module_xpath, module_xpath_iterate


class Form(BetterForm):
    EDIT_TEMPLATE = 'taoui_light_cone/edit.html'
    CONE = 'light-cone'
    BOX = 'box'
    UNIQUE = 'unique'
    RANDOM = 'random'
    MODULE_VERSION = 1
    SUMMARY_TEMPLATE = 'taoui_light_cone/summary.html'
    LABEL = 'General Properties'

    catalogue_geometry = forms.ChoiceField(choices=[(CONE, 'Light-Cone'), (BOX, 'Box')])

    redshift_max = forms.DecimalField(required=False, label=_('Redshift Max'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20', 'class': 'light_cone_field'}))
    redshift_min = forms.DecimalField(required=False, label=_('Redshift Min'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20', 'class': 'light_cone_field'}))

    box_size = forms.DecimalField(required=False, label=_('Box Size'), widget=forms.TextInput(attrs={'class': 'light_box_field'}))

    ra_opening_angle = forms.DecimalField(required=False, label=_('Right Ascension Opening Angle (degrees)'), min_value=0, max_value=360, max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20', 'class': 'light_cone_field'}))
    dec_opening_angle = forms.DecimalField(required=False, label=_('Declination Opening Angle (degrees)'), min_value=0, max_value=360, max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20', 'class': 'light_cone_field'}))

    light_cone_choices = [(UNIQUE, 'Unique'), (RANDOM, 'Random')]
    light_cone_type = forms.ChoiceField(required=False, initial=UNIQUE, label='', choices=light_cone_choices, widget=forms.RadioSelect(attrs={'class': 'light_cone_field'}))

    LIGHT_CONE_REQUIRED_FIELDS = ('ra_opening_angle', 'dec_opening_angle', 'redshift_min', 'redshift_max', 'light_cone_type', 'number_of_light_cones')  # Ensure these fields have a class of 'light_cone_field'
    BOX_REQUIRED_FIELDS = ('box_size', 'snapshot',)
    SEMIREQUIRED_FIELDS = LIGHT_CONE_REQUIRED_FIELDS + BOX_REQUIRED_FIELDS

    class Meta:
        fieldsets = [
            ('primary', {
                'legend': 'Data Selection',
                'fields': ['catalogue_geometry', 'dark_matter_simulation', 'galaxy_model',
                           'ra_opening_angle', 'dec_opening_angle', 'box_size', 'snapshot', 'redshift_min', 'redshift_max', 'light_cone_type', 'number_of_light_cones'],
            }),
            ('secondary',{
                'legend': 'Output properties',
                'fields': ['output_properties',],
            }),
            ]

    def __init__(self, *args, **kwargs):
        self.ui_holder = args[0]
        super(Form, self).__init__(*args[1:], **kwargs)

        if self.is_bound:
            dataset_id = self.data[self.prefix + '-galaxy_model']
            objs = datasets.output_choices(dataset_id)
            output_choices = [(x.id, x.label) for x in objs]
        else:
            output_choices = []

        self.fields['dark_matter_simulation'] = ChoiceFieldWithOtherAttrs(choices=datasets.dark_matter_simulation_choices())
        self.fields['galaxy_model'] = ChoiceFieldWithOtherAttrs(choices=datasets.galaxy_model_choices())
        self.fields['snapshot'] = ChoiceFieldWithOtherAttrs(required=False, choices=datasets.snapshot_choices(), widget=SelectWithOtherAttrs(attrs={'class': 'light_box_field'}))
        self.fields['number_of_light_cones'] = forms.IntegerField(label=_('Select the number of light-cones:'), required=False, initial='1')
        self.fields['output_properties'] = bf_fields.forms.MultipleChoiceField(required=True, choices=output_choices, widget=TwoSidedSelectWidget)

        for field_name in Form.SEMIREQUIRED_FIELDS:
            self.fields[field_name].semirequired = True
            self.context = {
                'simulations': tao_models.Simulation.objects.all(),
                'data_sets': tao_models.DataSet.objects.select_related('galaxy_model').all(),
            }
        self.fields['snapshot'].label = 'Redshift'

    def check_redshift_min_less_than_redshift_max(self):
        redshift_min_field = self.cleaned_data.get('redshift_min')
        redshift_max_field = self.cleaned_data.get('redshift_max')
        if redshift_min_field is not None and redshift_max_field is not None and redshift_min_field >= redshift_max_field:
            msg = _('The minimum redshift must be less than the maximum redshift.')
            self._errors["redshift_min"] = self.error_class([msg])
            del self.cleaned_data["redshift_min"]

    def check_light_cone_required_fields(self):
        catalogue_geometry = self.cleaned_data.get('catalogue_geometry')
        if catalogue_geometry == self.CONE:
            for field_name in self.LIGHT_CONE_REQUIRED_FIELDS:
                field = self.cleaned_data.get(field_name)
                if field is None and field_name not in self._errors:
                    self.errors[field_name] = self.error_class(['This field is required.'])

    def check_box_size_required_fields(self):
        catalogue_geometry = self.cleaned_data.get('catalogue_geometry')

        if catalogue_geometry == self.BOX:
            snapshot = self.cleaned_data.get('snapshot')
            if (snapshot is None or snapshot == '') and 'snapshot' not in self._errors:
                self.errors['snapshot'] = self.error_class(['This field is required.'])
            simulation = tao_models.Simulation.objects.get(pk=self.cleaned_data['dark_matter_simulation'])
            box_size = self.cleaned_data.get('box_size')
            if (box_size is not None) and box_size != '':
                if simulation.box_size < box_size:
                    self.errors['box_size'] = self.error_class(['Cannot be greater than box size of the simulation.'])
                if box_size <= 0:
                    self.errors['box_size'] = self.error_class(['Must be greater than zero.'])

    def clean(self):
        self.cleaned_data = super(Form, self).clean()
        self.check_redshift_min_less_than_redshift_max()
        self.check_box_size_required_fields()
        self.check_light_cone_required_fields()
        return self.cleaned_data

    def to_xml(self, root):
        from tao.xml_util import find_or_create, child_element

        light_cone_elem = find_or_create(root, 'light-cone')

        simulation = tao_models.Simulation.objects.get(pk=self.cleaned_data['dark_matter_simulation'])
        dataset = tao_models.DataSet.objects.get(id=self.cleaned_data['galaxy_model'])
        galaxy_model = dataset.galaxy_model

        child_element(light_cone_elem, 'module-version', text=Form.MODULE_VERSION)
        child_element(light_cone_elem, 'geometry', text=self.cleaned_data['catalogue_geometry'])
        child_element(light_cone_elem, 'simulation', text=simulation.name)
        child_element(light_cone_elem, 'galaxy-model', text=galaxy_model.name)

        if self.cleaned_data['catalogue_geometry'] == Form.BOX:
            snapshot = tao_models.Snapshot.objects.get(id=self.cleaned_data['snapshot'])
            child_element(light_cone_elem, 'redshift', text=snapshot.redshift)
        else:
            child_element(light_cone_elem, 'box-repetition', text=self.cleaned_data['light_cone_type'])
            child_element(light_cone_elem, 'num-cones', text=self.cleaned_data['number_of_light_cones'])
            child_element(light_cone_elem, 'redshift-min', text=self.cleaned_data['redshift_min'])
            child_element(light_cone_elem, 'redshift-max', text=self.cleaned_data['redshift_max'])

        if self.cleaned_data['catalogue_geometry'] == Form.CONE:
            child_element(light_cone_elem, 'ra-min', text='0.0', units='deg')
            child_element(light_cone_elem, 'ra-max', text=self.cleaned_data['ra_opening_angle'], units='deg')
            child_element(light_cone_elem, 'dec-min', text='0.0', units='deg')
            child_element(light_cone_elem, 'dec-max', text=self.cleaned_data['dec_opening_angle'], units='deg')

        if self.cleaned_data['catalogue_geometry'] == Form.BOX:
            box_size = self.cleaned_data['box_size']
            if box_size is None or box_size == '':
                box_size = simulation.box_size
            child_element(light_cone_elem, 'query-box-size', text=box_size, units='Mpc')

        output_properties = self.cleaned_data['output_properties']
        if len(output_properties) > 0:
            output_elem = child_element(light_cone_elem, 'output-fields')
            for item in output_properties:
                op = datasets.output_property(item)
                attrs = {'label': op.label}
                if op.units is not None and len(op.units) > 0: attrs['units'] = op.units
                child_element(output_elem, 'item', text=op.name, **attrs)

    @classmethod
    def from_xml(cls, ui_holder, xml_root, prefix=None):
        simulation = module_xpath(xml_root, '//light-cone/simulation')
        galaxy_model = module_xpath(xml_root, '//light-cone/galaxy-model')
        data_set = datasets.dataset_find_from_xml(simulation, galaxy_model)
        geometry = module_xpath(xml_root, '//light-cone/geometry')
        if not (geometry in [Form.CONE, Form.BOX]):
            geometry = None
        params = {
            prefix+'-catalogue_geometry': geometry,
            prefix+'-galaxy_model': data_set.id,
            }
        return cls(ui_holder, params, prefix=prefix)
    