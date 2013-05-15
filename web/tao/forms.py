"""
==================
tao.forms
==================

Settings for development environment
"""
from django import forms
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField

from form_utils.forms import BetterForm

import tao.settings as tao_settings
from tao import datasets
from tao.models import UserProfile, DataSetProperty, BandPassFilter
from tao.xml_util import module_xpath

NO_FILTER = 'no_filter'

class LoginForm(auth_forms.AuthenticationForm):
    remember_me = forms.BooleanField(label=_("Remember Me"), required=False)
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = 'autofocus'


class UserCreationForm(auth_forms.UserCreationForm):
    title = forms.CharField(label=_("Title"),
                            max_length=5)
    first_name = forms.CharField(label=_("First Name"),
                                    max_length=30)
    last_name = forms.CharField(label=_("Last Name"),
                                    max_length=30)
    institution = forms.CharField(label=_("Institution"), max_length=100)
    scientific_interests = forms.CharField(label=_("Scientific Interests"),
                                            help_text = _("e.g. your area of expertise, how you hope to use the data, team memberships and collaborations"),
                                            max_length=500,
                                            widget=forms.Textarea(attrs={'rows':
                                            3}), required=False)
    email = forms.EmailField(label=_("Email"), max_length=75)
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if not getattr(settings, 'USE_CAPTCHA', True):    
            del self.fields['captcha']

    class Meta:
        model = User
        fields = ('title', 'first_name', 'last_name', 'username', 'email',
        'password1', 'password2', 'institution', 'scientific_interests')


    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long'))
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).count() > 0:
            raise ValidationError(_('That email is already taken.'))
        return email

    def save(self):  # what about transactions?
        user = super(auth_forms.UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # FIXME shouldn't have to do this ??
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_active = False
        user.save()

        up = UserProfile(user=user)
        up.title = self.cleaned_data['title']
        up.institution = self.cleaned_data.get('institution')
        up.scientific_interests = self.cleaned_data.get('scientific_interests')
        up.save()

        return user

class RejectForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

class SupportForm(forms.Form):
    subject = forms.CharField(max_length=80, validators=[RegexValidator(regex='[^ \t\n\r\f\v,]', message="This field cannot be blank")], required=True)
    message = forms.CharField(widget=forms.Textarea(), validators=[RegexValidator(regex='[^ \t\n\r\f\v,]', message="This field cannot be blank")], required=True)


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
        from tao.xml_util import find_or_create, child_element

        # Hunt down the full item from the list of output formats.
        fmt = self.cleaned_data['supported_formats']
        ext = ''
        for x in tao_settings.OUTPUT_FORMATS:
            if x['value'] == fmt:
                ext = '.' + x['extension']
                break

        # The output file should be a CSV, by default.
        of_elem = find_or_create(parent_xml_element, fmt, module=fmt)
        child_element(of_elem, 'module-version', text=OutputFormatForm.MODULE_VERSION)
        child_element(of_elem, 'filename', text='tao.output' + ext)

    @classmethod
    def from_xml(cls, ui_holder, xml_root, prefix=None):
        supported_format = 'csv'
        return cls(ui_holder, {prefix + '-supported_formats': supported_format}, prefix=prefix)

class RecordFilterForm(BetterForm):
    EDIT_TEMPLATE = 'mock_galaxy_factory/record_filter.html'
    MODULE_VERSION = 1
    SUMMARY_TEMPLATE = 'mock_galaxy_factory/record_filter_summary.html'
    LABEL = 'Selection'

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
            objs = datasets.filter_choices(self.ui_holder.raw_data('light_cone', 'galaxy_model'))
            choices = [('X-' + NO_FILTER, 'No Filter')] + [('D-' + str(x.id), x.label + ' (' + x.units + ')') for x in objs] + [('B-' + str(x.id), x.label) for x in datasets.band_pass_filters_objects()]
            filter_type, record_filter = args[1]['record_filter-filter'].split('-')
            if filter_type == 'D':
                obj = DataSetProperty.objects.get(pk = record_filter)
                is_int = obj.data_type == DataSetProperty.TYPE_INT or obj.data_type == DataSetProperty.TYPE_LONG_LONG
        else:
            choices = [('X-' + NO_FILTER, 'No Filter')]
        if is_int:
            args = {'required': False,  'decimal_places': 0, 'max_digits': 20, 'widget': forms.TextInput(attrs={'maxlength': '20'})}
            val_class = forms.DecimalField
        else:
            args = {'required': False,  'widget': forms.TextInput(attrs={'maxlength': '20'})}
            val_class = forms.FloatField
        self.fields['filter'] = forms.ChoiceField(required=True, choices=choices)
        self.fields['max'] = val_class(**dict(args.items()+{'label':_('Max'),}.items()))
        self.fields['min'] = val_class(**dict(args.items()+{'label':_('Min'),}.items()))
        self.fields['filter'].label = 'Select by ...'

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

    def to_xml(self, parent_xml_element):
        from tao.xml_util import find_or_create, child_element

        selected_type, selected_filter = self.cleaned_data['filter'].split('-')
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
            filter_parameter = datasets.band_pass_filter(selected_filter)
            filter_type = filter_parameter.filter_id
            units = 'bpunits'

        rf_elem = find_or_create(parent_xml_element, 'record-filter')
        child_element(rf_elem, 'module-version', text=RecordFilterForm.MODULE_VERSION)
        child_element(rf_elem, 'filter-type', filter_type)
        filter_min = self.cleaned_data['min']
        filter_max = self.cleaned_data['max']
        default_filter = datasets.default_filter_choice(self.ui_holder.raw_data('light_cone', 'galaxy_model'))
        if default_filter is not None and filter_parameter.id == default_filter.id and filter_min is None and filter_max is None:
            filter_min = datasets.default_filter_min(self.ui_holder.raw_data('light_cone', 'galaxy_model'))
            filter_max = datasets.default_filter_max(self.ui_holder.raw_data('light_cone', 'galaxy_model'))
        child_element(rf_elem, 'filter-min', text=str(filter_min), units=units)
        child_element(rf_elem, 'filter-max', text=str(filter_max), units=units)

    @classmethod
    def from_xml(cls, ui_holder, xml_root, prefix=None):
        simulation = module_xpath(xml_root, '//light-cone/simulation')
        galaxy_model = module_xpath(xml_root, '//light-cone/galaxy-model')
        data_set = datasets.dataset_find_from_xml(simulation, galaxy_model)
        filter_type = module_xpath(xml_root, '//record-filter/filter-type')
        filter_min = module_xpath(xml_root, '//record-filter/filter-min')
        filter_max = module_xpath(xml_root, '//record-filter/filter-max')
        filter_units = module_xpath(xml_root, '//record-filter/filter-min', attribute='units')
        if filter_min == 'None': filter_min = None
        if filter_max == 'None': filter_max = None
        data_set_id = 0
        if data_set is not None: data_set_id = data_set.id
        kind, record_id = datasets.filter_find_from_xml(data_set_id, filter_type, filter_units)
        if filter_type == None:
            kind = 'X'
            record_id = NO_FILTER
        attrs = {prefix+'-filter': kind + '-' + str(record_id),
               prefix+'-min': filter_min,
               prefix+'-max': filter_max,
               }
        return cls(ui_holder, attrs, prefix=prefix)
