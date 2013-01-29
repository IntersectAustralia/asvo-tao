from django import forms
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField

from form_utils.forms import BetterForm

import tao.settings as tao_settings
from tao import datasets
from tao.models import UserProfile, DataSetProperty

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

class OutputFormatForm(BetterForm):
    EDIT_TEMPLATE = 'mock_galaxy_factory/output_format.html'
    MODULE_VERSION = 1
    SUMMARY_TEMPLATE = 'mock_galaxy_factory/output_format_summary.html'

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

        of_elem = find_or_create(parent_xml_element, 'output-file')
        child_element(of_elem, 'module-version', text=OutputFormatForm.MODULE_VERSION)
        child_element(of_elem, 'format', text=self.cleaned_data['supported_formats'])

class RecordFilterForm(BetterForm):
    EDIT_TEMPLATE = 'mock_galaxy_factory/record_filter.html'
    MODULE_VERSION = 1
    SUMMARY_TEMPLATE = 'mock_galaxy_factory/record_filter_summary.html'

    max = forms.DecimalField(required=False, label=_('Max'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20'}))
    min = forms.DecimalField(required=False, label=_('Min'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20'}))


    class Meta:
        fieldsets = [('primary', {
            'legend': '',
            'fields': ['filter', 'min', 'max',],
        }),]

    def __init__(self, *args, **kwargs):
        self.ui_holder = args[0]
        super(RecordFilterForm, self).__init__(*args[1:], **kwargs)
        if self.ui_holder.is_bound('light_cone'):
            objs = datasets.filter_choices(self.ui_holder.raw_data('light_cone', 'galaxy_model'))
            choices = [(NO_FILTER, 'No Filter')] + [(x.id, '') for x in objs]
        else:
            choices = [(NO_FILTER, 'No Filter')]
        self.fields['filter'] = forms.ChoiceField(required=True, choices=choices)

    def check_min_less_than_max(self):
        min_field = self.cleaned_data.get('min')
        max_field = self.cleaned_data.get('max')
        if min_field is not None and max_field is not None and min_field >= max_field:
            msg = _('The "min" field must be less than the "max" field.')
            self._errors["min"] = self.error_class([msg])
            del self.cleaned_data["min"]

    def clean(self):
        super(RecordFilterForm, self).clean()
        self.check_min_less_than_max()
        return self.cleaned_data

    def to_xml(self, parent_xml_element):
        from tao.xml_util import find_or_create, child_element

        selected_filter = self.cleaned_data['filter']
        if selected_filter == NO_FILTER:
            return

        filter_parameter = DataSetProperty.objects.get(pk=selected_filter)

        rf_elem = find_or_create(parent_xml_element, 'record-filter')
        child_element(rf_elem, 'module-version', text=RecordFilterForm.MODULE_VERSION)
        child_element(rf_elem, 'filter-type', filter_parameter.name)
        filter_min = self.cleaned_data['min']
        filter_max = self.cleaned_data['max']
        child_element(rf_elem, 'filter-min', text=str(filter_min), units=filter_parameter.units)
        child_element(rf_elem, 'filter-max', text=str(filter_max), units=filter_parameter.units)




