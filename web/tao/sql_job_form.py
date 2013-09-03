from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from form_utils.forms import BetterForm
import form_utils.fields as bf_fields
from tao.widgets import ChoiceFieldWithOtherAttrs, SelectWithOtherAttrs, TwoSidedSelectWidget, SpinnerWidget

from tao import datasets
from tao.models import DataSetProperty
from tao.xml_util import module_xpath, module_xpath_iterate

def from_xml_2(cls, ui_holder, xml_root, prefix=None):
    query = module_xpath(xml_root, '//sql/query')
    simulation_name = module_xpath(xml_root, '//sql/simulation')
    galaxy_model_name = module_xpath(xml_root, '//sql/galaxy-model')
    output_properties = module_xpath(xml_root, '//votable/fields/item')
    simulation = datasets.simulation_from_xml(simulation_name)
    galaxy_model = datasets.galaxy_model_from_xml(galaxy_model_name)
    data_set = datasets.dataset_find_from_xml(simulation, galaxy_model)
    output_properties = [dsp for dsp in SQLJobForm._map_elems(xml_root)]
    query = query.replace('-table-', data_set.database)
    simulation_id = None
    if simulation is not None: simulation_id = simulation.id
    galaxy_model_id = None
    if galaxy_model is not None: galaxy_model_id = galaxy_model.id
    params = {
        prefix+'-galaxy_model': galaxy_model_id,
        prefix+'-dark_matter_simulation': simulation_id,
        prefix+'-query': query,
        prefix+'-output_properties': output_properties,
        }
    return cls(ui_holder, params, prefix=prefix)

class SQLJobForm(BetterForm):
    SUMMARY_TEMPLATE = 'jobs/sql_job_summary.html'
    simple_fields = ['dark_matter_simulation', 'galaxy_model']
    fieldsets = [
            ('primary', {
                'legend': 'Data Selection',
                'fields': simple_fields,
                'query': '',
            }),]

    def __init__(self, *args, **kwargs):
        self.ui_holder = args[0]
        super(SQLJobForm, self).__init__(*args[1:], **kwargs)
        is_int = False
        
        #self.fields['query'].widget.attrs['data-bind'] = ''
        self.fields['query'] = forms.CharField()
        self.fields['dark_matter_simulation'] = ChoiceFieldWithOtherAttrs(choices=[])
        self.fields['galaxy_model'] = ChoiceFieldWithOtherAttrs(choices=[])
        self.fields['output_properties'] = bf_fields.forms.MultipleChoiceField(required=False, choices=[], widget=TwoSidedSelectWidget)
        
        self.fields['query'].widget.attrs['data-bind'] = 'value: query'
        self.fields['dark_matter_simulation'].widget.attrs['data-bind'] = 'options: dark_matter_simulations, value: dark_matter_simulation, optionsText: function(i) { return i.fields.name}, event: {change: function() { box_size(dark_matter_simulation().fields.box_size); }}'
        self.fields['galaxy_model'].widget.attrs['data-bind'] = 'options: galaxy_models, value: galaxy_model, optionsText: function(i) { return i.fields.name }'
        self.fields['output_properties'].widget.attrs['ko_data'] = {'widget':'output_properties_widget','value':'output_properties'}

    def clean(self):
        super(SQLJobForm, self).clean()
        return self.cleaned_data

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
        
    @classmethod
    def _map_elems(cls, xml_root):
        for elem in module_xpath_iterate(xml_root, '//votable/fields/item', text=False):
            label = elem.get('label')
            units = elem.get('units')
            name  = elem.text
            yield {'label': label, 'units': units, 'name': name}
            
        
