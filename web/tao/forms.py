from django import forms
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField

from form_utils.forms import BetterForm

from tao import datasets
from tao.models import UserProfile

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


from tao.widgets import ChoiceFieldWithOtherAttrs

class SEDForm(BetterForm):
    class Meta:
        fieldsets = [('primary', {
            'legend': 'Model',
            'fields': ['single_stellar_population_model'],
        }),]

    def __init__(self, *args, **kwargs):
        super(SEDForm, self).__init__(*args, **kwargs)
        self.fields['single_stellar_population_model'] = ChoiceFieldWithOtherAttrs(choices=datasets.stellar_model_choices())


class LightConeForm(BetterForm):
    CONE = 'cone'
    BOX = 'box'

    catalogue_geometry = forms.ChoiceField(choices=[(CONE, 'Light-Cone'), (BOX, 'Box')])

    max = forms.DecimalField(required=False, label=_('Max'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20'}))
    min = forms.DecimalField(required=False, label=_('Min'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20'}))
    redshift_max = forms.DecimalField(required=False, label=_('Redshift Max'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20', 'class': 'light_cone_field'}))
    redshift_min = forms.DecimalField(required=False, label=_('Redshift Min'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20', 'class': 'light_cone_field'}))
    box_size = forms.DecimalField(required=False, label=_('Box Size'))

    ra_max = forms.DecimalField(required=False, label=_('RA max (degrees)'), min_value=0, max_value=360, max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20', 'class': 'light_cone_field'}))
    dec_max = forms.DecimalField(required=False, label=_('dec max (degrees)'), min_value=0, max_value=360, max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20', 'class': 'light_cone_field'}))

    LIGHT_CONE_REQUIRED_FIELDS = ('ra_max', 'dec_max', 'redshift_min', 'redshift_max',)  # Ensure these fields have a class of 'light_cone_field'
    BOX_REQUIRED_FIELDS = ('box_size',)
    SEMIREQUIRED_FIELDS = LIGHT_CONE_REQUIRED_FIELDS + BOX_REQUIRED_FIELDS

    class Meta:
        fieldsets = [('primary', {
            'legend': 'General',
            'fields': ['catalogue_geometry', 'dark_matter_simulation', 'galaxy_model',
            'ra_max', 'dec_max', 'box_size', 'redshift_min', 'redshift_max',],
        }), ('secondary', {
            'legend': 'Parameters',
            'fields': ['filter', 'min', 'max',],
        }),]

    def __init__(self, *args, **kwargs):
        super(LightConeForm, self).__init__(*args, **kwargs)
        self.fields['dark_matter_simulation'] = ChoiceFieldWithOtherAttrs(choices=datasets.dark_matter_simulation_choices())
        self.fields['galaxy_model'] = ChoiceFieldWithOtherAttrs(choices=datasets.galaxy_model_choices())
        self.fields['filter'] = ChoiceFieldWithOtherAttrs(choices=datasets.filter_choices())
        for field_name in LightConeForm.SEMIREQUIRED_FIELDS:
            self.fields[field_name].semirequired = True

    def check_min_less_than_max(self):
        min_field = self.cleaned_data.get('min')
        max_field = self.cleaned_data.get('max')
        if min_field is not None and max_field is not None and min_field >= max_field:
            msg = _('The "min" field must be less than the "max" field.')
            self._errors["min"] = self.error_class([msg])
            del self.cleaned_data["min"]

    def check_redshift_min_less_than_redshift_max(self):
        redshift_min_field = self.cleaned_data.get('redshift_min')
        redshift_max_field = self.cleaned_data.get('redshift_max')
        if redshift_min_field is not None and redshift_max_field is not None and redshift_min_field >= redshift_max_field:
            msg = _('The "Rmin" field must be less than the "Rmax" field.')
            self._errors["redshift_min"] = self.error_class([msg])
            del self.cleaned_data["redshift_min"]

    def check_light_cone_required_fields(self):
        catalogue_geometry = self.cleaned_data.get('catalogue_geometry')
        if catalogue_geometry == 'cone':
            for field_name in self.LIGHT_CONE_REQUIRED_FIELDS:
                field = self.cleaned_data.get(field_name)
                if field is None and field_name not in self._errors:
                    self.errors[field_name] = self.error_class(['This field is required.'])

    def check_box_size_required_for_box(self):
        catalogue_geometry_field = self.cleaned_data.get('catalogue_geometry')
        box_size_field = self.cleaned_data.get('box_size')
        if catalogue_geometry_field == 'box' and box_size_field is None:
            msg = _('The "Box Size" field is required when "Box" is selected')
            self._errors["box_size"] = self.error_class([msg])
            del self.cleaned_data['catalogue_geometry']

    def clean(self):
        self.cleaned_data = super(LightConeForm, self).clean()
        self.check_min_less_than_max()
        self.check_redshift_min_less_than_redshift_max()
        self.check_box_size_required_for_box()
        self.check_light_cone_required_fields()

        return self.cleaned_data
