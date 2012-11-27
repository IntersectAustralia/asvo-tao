from django import forms
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField

from form_utils.forms import BetterForm

from tao import datasets, models
from tao.models import UserProfile

class LoginForm(auth_forms.AuthenticationForm):
    remember_me = forms.BooleanField(label=_("Remember Me"), required=False)


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

class MockGalaxyFactoryForm(BetterForm):
    max = forms.DecimalField(required=False, label=_('Max/Faintest'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20'}))
    min = forms.DecimalField(required=False, label=_('Min/Brightest'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20'}))
    rmax = forms.DecimalField(required=False, label=_('Rmax'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20'}))
    rmin = forms.DecimalField(required=False, label=_('Rmin'), max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20'}))
    box_size = forms.DecimalField(required=False, label=_('Box Size'))

    ra = forms.DecimalField(required=False, label=_('RA'), min_value=0, max_value=5400, max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20', 'class': 'light_cone_field'}))
    dec = forms.DecimalField(required=False, label=_('dec'), min_value=0, max_value=5400, max_digits=20, widget=forms.TextInput(attrs={'maxlength': '20', 'class': 'light_cone_field'}))
    
    class Meta:
        fieldsets = [('primary', {
            'legend': 'General',
            'fields': ['box_type', 'dark_matter_simulation', 'galaxy_model', 'ra', 'dec', 'box_size'],
        }), ('secondary', {
            'legend': 'Parameters',
            'fields': ['filter', 'max', 'min', 'rmax', 'rmin'],
        }), ('third', {
            'legend': 'Output properties',
            'fields': [],
        }), ('fourth', {
            'legend': 'Miscellaneous',
            'fields': [],
        }),]

    def __init__(self, *args, **kwargs):
        super(MockGalaxyFactoryForm, self).__init__(*args, **kwargs)
        self.fields['box_type'] = ChoiceFieldWithOtherAttrs(choices=[('cone', 'Light-Cone', {}), ('box', 'Box', {})])
        self.fields['dark_matter_simulation'] = ChoiceFieldWithOtherAttrs(choices=datasets.dark_matter_simulation_choices())
        self.fields['galaxy_model'] = ChoiceFieldWithOtherAttrs(choices=datasets.galaxy_model_choices())
        self.fields['filter'] = ChoiceFieldWithOtherAttrs(choices=datasets.filter_choices())
        for field_name in ['ra', 'dec', 'box_size']:
            self.fields[field_name].semirequired = True
        
    def check_min_less_than_max(self):
        min_field = self.cleaned_data.get('min')
        max_field = self.cleaned_data.get('max')
        if min_field is not None and max_field is not None and min_field >= max_field:
            msg = _('The "min" field must be less than the "max" field.')
            self._errors["min"] = self.error_class([msg])
            del self.cleaned_data["min"]
    
    def check_rmin_less_than_rmax(self):
        rmin_field = self.cleaned_data.get('rmin')
        rmax_field = self.cleaned_data.get('rmax')
        if rmin_field is not None and rmax_field is not None and rmin_field >= rmax_field:
            msg = _('The "Rmin" field must be less than the "Rmax" field.')
            self._errors["rmin"] = self.error_class([msg])
            del self.cleaned_data["rmin"]

    def check_light_cone_required_fields(self):
        box_type = self.cleaned_data.get('box_type')
        if box_type == 'cone':
            ra = self.cleaned_data.get('ra')
            dec = self.cleaned_data.get('dec')
            if ra is None and 'ra' not in self._errors:
                self._errors['ra'] = self.error_class(['This field is required.'])
            if dec is None and 'dec' not in self._errors:
                self._errors['dec'] = self.error_class(['This field is required.'])
        
    def check_box_size_required_for_box(self):
        box_type_field = self.cleaned_data.get('box_type')
        box_size_field = self.cleaned_data.get('box_size')
        if box_type_field == 'box' and box_size_field is None:
            msg = _('The "Box Size" field is required when "Box" is selected')
            self._errors["box_size"] = self.error_class([msg])
            del self.cleaned_data['box_type']
        
    def clean(self):
        self.cleaned_data = super(MockGalaxyFactoryForm, self).clean()
        self.check_min_less_than_max()
        self.check_rmin_less_than_rmax()
        self.check_box_size_required_for_box()
        self.check_light_cone_required_fields()
        
        return self.cleaned_data
        
    def save(self, user):
        job = models.Job(user=user)
        job.save()
        return job
