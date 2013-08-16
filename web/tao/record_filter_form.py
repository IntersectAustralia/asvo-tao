from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from form_utils.forms import BetterForm

from tao import datasets
from tao.forms import NO_FILTER
from tao.models import DataSetProperty
from tao.xml_util import module_xpath

#### XML version 2 ####

def to_xml_2(form, root):
   from tao.xml_util import find_or_create, child_element

   selected_type, selected_filter = form.cleaned_data['filter'].split('-')
   if selected_filter == NO_FILTER:
       return

   filter_parameter = None
   filter_type = ''
   units = ''
   if selected_type == 'D':
       filter_parameter = DataSetProperty.objects.get(pk=selected_filter)
       filter_type = filter_parameter.name
       units = filter_parameter.units
   elif selected_type == 'B':
       selected_filter, selected_extension = selected_filter.split('_')
       filter_parameter = datasets.band_pass_filter(selected_filter)
       filter_type = str(filter_parameter.filter_id) + '_' + selected_extension
       units = 'bpunits'

   rf_elem = find_or_create(root, 'record-filter')
   child_element(rf_elem, 'module-version', text=RecordFilterForm.MODULE_VERSION)
   filter_elem = find_or_create(rf_elem, 'filter')
   child_element(filter_elem, 'filter-attribute', filter_type)
   filter_min = form.cleaned_data['min']
   filter_max = form.cleaned_data['max']
   default_filter = form.ui_holder.dataset.default_filter_field
   if default_filter is not None and filter_parameter.id == default_filter.id and filter_min is None and filter_max is None:
       filter_min = form.ui_holder.dataset.default_filter_min
       filter_max = form.ui_holder.dataset.default_filter_max
   child_element(filter_elem, 'filter-min', text=str(filter_min), units=units)
   child_element(filter_elem, 'filter-max', text=str(filter_max), units=units)

def from_xml_2(cls, ui_holder, xml_root, prefix=None):
   simulation = module_xpath(xml_root, '//light-cone/simulation')
   galaxy_model = module_xpath(xml_root, '//light-cone/galaxy-model')
   data_set = datasets.dataset_find_from_xml(simulation, galaxy_model)
   filter_attribute = module_xpath(xml_root, '//record-filter/filter/filter-attribute')
   filter_min = module_xpath(xml_root, '//record-filter/filter/filter-min')
   filter_max = module_xpath(xml_root, '//record-filter/filter/filter-max')
   filter_units = module_xpath(xml_root, '//record-filter/filter/filter-min', attribute='units')
   if filter_min == 'None': filter_min = None
   if filter_max == 'None': filter_max = None
   data_set_id = 0
   if data_set is not None: data_set_id = data_set.id
   kind, record_id = datasets.filter_find_from_xml(data_set_id, filter_attribute, filter_units)
   if filter_attribute == None:
       kind = 'X'
       record_id = NO_FILTER
   attrs = {prefix+'-filter': kind + '-' + str(record_id),
            prefix+'-min': filter_min,
            prefix+'-max': filter_max,
            }
   return cls(ui_holder, attrs, prefix=prefix)

########################

class RecordFilterForm(BetterForm):
    EDIT_TEMPLATE = 'mock_galaxy_factory/record_filter.html'
    MODULE_VERSION = 1
    SUMMARY_TEMPLATE = 'mock_galaxy_factory/record_filter_summary.html'
    LABEL = 'Selection'
    TAB_ID = settings.MODULE_INDICES['record_filter']

    class Meta:
        fieldsets = [('primary', {
            'legend': '',
            'fields': ['filter', 'min', 'max',],
        }),]

    def __init__(self, *args, **kwargs):
        self.ui_holder = args[0]
        super(RecordFilterForm, self).__init__(*args[1:], **kwargs)
        is_int = False
        if self.ui_holder.is_bound('light_cone'):
            objs = datasets.filter_choices(
                self.ui_holder.raw_data('light_cone', 'dark_matter_simulation'),
                self.ui_holder.raw_data('light_cone', 'galaxy_model'))
            choices = [('X-' + NO_FILTER, 'No Filter')] + [('D-' + str(x.id), x.label + ' (' + x.units + ')') for x in objs] + \
                [('B-' + str(x.id) + '_apparent', x.label) for x in datasets.band_pass_filters_objects()] + \
                [('B-' + str(x.id) + '_absolute', x.label) for x in datasets.band_pass_filters_objects()]
            filter_type, record_filter = args[1]['record_filter-filter'].split('-')
            if filter_type == 'D':
                obj = DataSetProperty.objects.get(pk = record_filter)
                is_int = obj.data_type == DataSetProperty.TYPE_INT or obj.data_type == DataSetProperty.TYPE_LONG_LONG
        else:
            choices = [] # [('X-' + NO_FILTER, 'No Filter')]
        if is_int:
            args = {'required': False,  'decimal_places': 0, 'max_digits': 20}
            val_class = forms.DecimalField
        else:
            args = {'required': False}
            val_class = forms.FloatField

        self.fields['filter'] = forms.ChoiceField(required=True, choices=choices)
        self.fields['max'] = val_class(**dict(args.items()+{'label':_('Max'), 'widget': forms.TextInput(attrs={'maxlength': '20'})}.items()))
        self.fields['min'] = val_class(**dict(args.items()+{'label':_('Min'), 'widget': forms.TextInput(attrs={'maxlength': '20'})}.items()))
        self.fields['filter'].label = 'Select by ...'

        self.fields['filter'].widget.attrs['data-bind'] = 'options: selections, value: selection, optionsText: function(i) { return i.label }, optionsValue: function(i) { return i.value }'
        self.fields['min'].widget.attrs['data-bind'] = 'value: selection_min'
        self.fields['max'].widget.attrs['data-bind'] = 'value: selection_max'


    def check_min_or_max_or_both(self):
        if 'filter' not in self.cleaned_data:
            return
        selected_type, selected_filter = self.cleaned_data['filter'].split('-')
        if selected_filter == NO_FILTER:
            return
        min_field = self.cleaned_data.get('min')
        max_field = self.cleaned_data.get('max')
        if min_field is None and max_field is None:
            msg = _('Either "min", "max" or both to be provided.')
            self._errors["min"] = self.error_class([msg])
            self._errors["max"] = self.error_class([msg])

    def check_min_less_than_max(self):
        min_field = self.cleaned_data.get('min')
        max_field = self.cleaned_data.get('max')
        if min_field is not None and max_field is not None and min_field >= max_field:
            msg = _('The "min" field must be less than the "max" field.')
            self._errors["min"] = self.error_class([msg])
            del self.cleaned_data["min"]

    def clean(self):
        super(RecordFilterForm, self).clean()
        self.check_min_or_max_or_both()
        self.check_min_less_than_max()
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

