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
from tao.forms import FormsGraph
from tao.widgets import ChoiceFieldWithOtherAttrs, SelectWithOtherAttrs, TwoSidedSelectWidget
from tao.xml_util import module_xpath, module_xpath_iterate

#### XML version 2 ####

def to_xml_2(form, root):
    from tao.xml_util import find_or_create, child_element

    light_cone_elem = find_or_create(root, 'light-cone', id=FormsGraph.LIGHT_CONE_ID)

    simulation = tao_models.Simulation.objects.get(pk=form.cleaned_data['dark_matter_simulation'])
    dataset = tao_models.DataSet.objects.get(id=form.cleaned_data['galaxy_model'])
    galaxy_model = dataset.galaxy_model

    child_element(light_cone_elem, 'module-version', text=Form.MODULE_VERSION)
    child_element(light_cone_elem, 'geometry', text=form.cleaned_data['catalogue_geometry'])
    child_element(light_cone_elem, 'simulation', text=simulation.name)
    child_element(light_cone_elem, 'galaxy-model', text=galaxy_model.name)

    if form.cleaned_data['catalogue_geometry'] == Form.BOX:

        snapshot = tao_models.Snapshot.objects.get(id=form.cleaned_data['snapshot'])
        child_element(light_cone_elem, 'redshift', text=snapshot.redshift)
        box_size = form.cleaned_data['box_size']
        if box_size is None or box_size == '':
            box_size = simulation.box_size
        child_element(light_cone_elem, 'query-box-size', text=box_size, units='Mpc')

    else:  # == Form.CONE

        child_element(light_cone_elem, 'box-repetition', text=form.cleaned_data['light_cone_type'])
        child_element(light_cone_elem, 'num-cones', text=form.cleaned_data['number_of_light_cones'])
        child_element(light_cone_elem, 'redshift-min', text=form.cleaned_data['redshift_min'])
        child_element(light_cone_elem, 'redshift-max', text=form.cleaned_data['redshift_max'])
        child_element(light_cone_elem, 'ra-min', text='0.0', units='deg')
        child_element(light_cone_elem, 'ra-max', text=form.cleaned_data['ra_opening_angle'], units='deg')
        child_element(light_cone_elem, 'dec-min', text='0.0', units='deg')
        child_element(light_cone_elem, 'dec-max', text=form.cleaned_data['dec_opening_angle'], units='deg')

    output_properties = form.cleaned_data['output_properties']
    if len(output_properties) > 0:

        # Create the light-cone output properties.
        output_elem = child_element(light_cone_elem, 'output-fields')

        # Either create or find the CSV/HDF5 output properties.
        output_format = form.ui_holder.cleaned_data('output_format', 'supported_formats')
        fields_elem = find_or_create(find_or_create(root, output_format, id=FormsGraph.OUTPUT_ID), 'fields')

        # Insert entries.
        for item in output_properties:
            op = datasets.output_property(item)
            attrs = {'label': op.label}
            if op.units is not None and len(op.units) > 0: attrs['units'] = op.units
            child_element(fields_elem, 'item', text=op.name, **attrs)
            attrs.update({'description': op.description})
            if not op.is_computed:
                child_element(output_elem, 'item', text=op.name, **attrs)

def from_xml_2(cls, ui_holder, xml_root, prefix=None):
    simulation_name = module_xpath(xml_root, '//light-cone/simulation')
    galaxy_model = module_xpath(xml_root, '//light-cone/galaxy-model')
    simulation = datasets.simulation_from_xml(simulation_name)
    data_set = datasets.dataset_find_from_xml(simulation_name, galaxy_model)
    geometry = module_xpath(xml_root, '//light-cone/geometry')
    simulation_id = None
    if simulation is not None: simulation_id = simulation.id
    data_set_id = None
    if data_set is not None: data_set_id = data_set.id
    if not (geometry in [Form.CONE, Form.BOX]):
        geometry = None
    params = {
        prefix+'-catalogue_geometry': geometry,
        prefix+'-galaxy_model': data_set_id,
        prefix+'-dark_matter_simulation': simulation_id,
        }

    if geometry == Form.BOX:

        redshift = module_xpath(xml_root, '//light-cone/redshift')
        snapshot = datasets.snapshot_from_xml(data_set, redshift)
        if snapshot is not None:
            params.update({prefix+'-snapshot':snapshot.id})
        box_size = module_xpath(xml_root, '//light-cone/query-box-size')
        params.update({prefix+'-box_size': box_size})

    else: ## == Form.CONE

        light_cone_type = module_xpath(xml_root, '//light-cone/box-repetition')
        num_cones = module_xpath(xml_root, '//light-cone/num-cones')
        redshift_min = module_xpath(xml_root, '//light-cone/redshift-min')
        redshift_max = module_xpath(xml_root, '//light-cone/redshift-max')
        ra_max = module_xpath(xml_root, '//light-cone/ra-max')
        dec_max = module_xpath(xml_root, '//light-cone/dec-max')
        params.update({
            prefix+'-light_cone_type': light_cone_type,
            prefix+'-number_of_light_cones': num_cones,
            prefix+'-redshift_min': redshift_min,
            prefix+'-redshift_max': redshift_max,
            prefix+'-ra_opening_angle': ra_max,
            prefix+'-dec_opening_angle': dec_max,
            })

    params.update({prefix+'-output_properties': [dsp.id for dsp in Form._map_elems(xml_root, data_set)]})
    return cls(ui_holder, params, prefix=prefix)

#######################

class Form(BetterForm):
    EDIT_TEMPLATE = 'taoui_light_cone/edit.html'
    CONE = 'light-cone'
    BOX = 'box'
    UNIQUE = 'unique'
    RANDOM = 'random'
    MODULE_VERSION = 1
    SUMMARY_TEMPLATE = 'taoui_light_cone/summary.html'
    LABEL = 'General Properties'

    catalogue_geometry = forms.ChoiceField(choices=[(BOX, 'Box'), (CONE, 'Light-Cone'), ])

    redshift_max = forms.DecimalField(required=False, label=_('Redshift Max'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20', 'class': 'light_cone_field'}))
    redshift_min = forms.DecimalField(required=False, label=_('Redshift Min'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20', 'class': 'light_cone_field'}))

    box_size = forms.DecimalField(required=False, label=_('Box Size (Mpc/h)'), widget=forms.TextInput(attrs={'class': 'light_box_field'}))

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
            sid = kwargs['light_cone-dark_matter_simulation']
        else:
            sid = datasets.dark_matter_simulation_choices()[0][0]
            dataset_id = datasets.galaxy_model_choices(sid)[0][0]
        objs = datasets.output_choices(dataset_id)
        output_choices = [(x.id, x.label) for x in objs]

        self.fields['dark_matter_simulation'] = ChoiceFieldWithOtherAttrs(choices=datasets.dark_matter_simulation_choices())
        self.fields['galaxy_model'] = ChoiceFieldWithOtherAttrs(choices=datasets.galaxy_model_choices(sid))
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

        ## Knockout data-bind
        self.fields['catalogue_geometry'].widget.attrs['data-bind'] = 'value: catalogue_geometry'
        self.fields['ra_opening_angle'].widget.attrs['data-bind'] = 'value: ra_opening_angle'
        self.fields['dec_opening_angle'].widget.attrs['data-bind'] = 'value: dec_opening_angle'
        self.fields['output_properties'].widget.attrs['ko_data'] = 'output_properties'

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
        version = 2.0
        to_xml_2(self, root)

    @classmethod
    def from_xml(cls, ui_holder, xml_root, prefix=None):
        version = module_xpath(xml_root, '//workflow/schema-version')
        if version == '2.0':
            return from_xml_2(cls, ui_holder, xml_root, prefix=prefix)
        else:
            return cls(ui_holder, prefix=prefix)

    @classmethod
    def _map_elems(cls, xml_root, data_set):
        for elem in module_xpath_iterate(xml_root, '//light-cone/output-fields/item', text=False):
            label = elem.get('label')
            name = elem.text
            data_set_property = datasets.data_set_property_from_xml(data_set, label, name)
            if data_set_property is not None:
                yield data_set_property

