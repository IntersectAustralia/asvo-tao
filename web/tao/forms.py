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

from tao.models import UserProfile

NO_FILTER = 'no_filter'

class FormsGraph():
    LIGHT_CONE_ID = '1'
    SED_ID = '2'
    DUST_ID = '3'
    BANDPASS_FILTER_ID = '4'
    OUTPUT_ID = '5'
    MOCK_IMAGE_ID = '6'

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
