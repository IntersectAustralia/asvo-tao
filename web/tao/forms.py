"""
==================
tao.forms
==================

Settings for development environment
"""
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.contrib.auth import forms as auth_forms, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.template import loader
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _
from captcha.fields import ReCaptchaField

from tao.models import TaoUser
NO_FILTER = 'no_filter'


class FormsGraph():
    LIGHT_CONE_ID = '1'
    SED_ID = '2'
    DUST_ID = '3'
    BANDPASS_FILTER_ID = '4'
    OUTPUT_ID = '5'
    MOCK_IMAGE_ID = '6'
    TELESCOPE_ID = '7'


class TaoPasswordChangeForm(PasswordChangeForm):

    def clean_new_password1(self):
        if hasattr(super(TaoPasswordChangeForm, self), 'clean_new_password1'):
            password1 = super(TaoPasswordChangeForm, self).clean_new_password1()
        else:
            password1 = self.cleaned_data['new_password1']
        if len(password1) < settings.MIN_PASSWORD_LENGTH:
            raise forms.ValidationError(_('Password must be at least %d characters long') % settings.MIN_PASSWORD_LENGTH)
        return password1


class PasswordResetForm(auth_forms.PasswordResetForm):
    username = forms.CharField(max_length=254, label=_("Username"), required=True)

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = 'autofocus'
        self.fields.keyOrder = ['username', 'email']
        self.error_messages['unknown_user'] = _("That username doesn't have an associated "
                                                "user account. Are you sure you've registered?")
        self.error_messages['wrong_email'] = _("That email doesn't match that of the user. "
                                               "Please check you have provided the email that you registered.")

    def clean_username(self):
        """
        Validates that an active user exists with the given username.
        """
        UserModel = get_user_model()
        username = self.cleaned_data["username"]
        self.users_cache = UserModel._default_manager.filter(username__iexact=username)
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown_user'])
        if not any(user.is_active for user in self.users_cache):
            # none of the filtered users are active
            raise forms.ValidationError(self.error_messages['unknown_user'])
        return username

    def clean_email(self):
        """
        Validates that the given email address matches that of the given user.
        """
        email = self.cleaned_data["email"]
        if not any(user.email == email for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['wrong_email'])
        return email

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a new random password, saves it, and sends to the
        user.
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        for user in self.users_cache:
            print domain_override
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            new_password = UserModel.objects.make_random_password()
            user.set_password(new_password)
            user.save()
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.pk),
                'user': user,
                # 'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
                'password': new_password,
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, from_email, [user.email])


class LoginForm(auth_forms.AuthenticationForm):
    remember_me = forms.BooleanField(label=_("Remember Me"), required=False)
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = 'autofocus'


class UserCreationForm(forms.Form):
    # username
    # password1
    # password2
    title = forms.CharField(label=_("Title"),
                            max_length=5)
    institution = forms.CharField(label=_("Institution"), max_length=100)
    scientific_interests = forms.CharField(label=_("Scientific Interests"),
                                            help_text = _("e.g. your area of expertise, how you hope to use the data, team memberships and collaborations"),
                                            max_length=500,
                                            widget=forms.Textarea(attrs={'rows':
                                            3}), required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs['user']
        super(UserCreationForm, self).__init__(*args)
        if self.is_aaf():
            self.create_aaf_fields()
        else:
            self.create_fields()

    def create_aaf_fields(self):
        first_name = forms.CharField(label=_("First Name"), max_length=30, initial=self.user.first_name)
        first_name.widget.attrs['readonly'] = True
        self.fields['first_name'] = first_name
        last_name = forms.CharField(label=_("Last Name"), max_length=30, initial=self.user.last_name)
        last_name.widget.attrs['readonly'] = True
        self.fields['last_name'] = last_name
        email = forms.EmailField(label=_("Email"), max_length=75, initial=self.user.email)
        email.widget.attrs['readonly'] = True
        self.fields['email'] = email
        username = forms.CharField(label=_("Username"), max_length=75, initial='from AAF')
        username.widget.attrs['readonly'] = True
        self.fields['username'] = username
        self.fields.keyOrder = ('title', 'first_name', 'last_name', 'username', 'email',
            'institution', 'scientific_interests')

    def create_fields(self):
        first_name = forms.CharField(label=_("First Name"), max_length=30)
        self.fields['first_name'] = first_name
        last_name = forms.CharField(label=_("Last Name"), max_length=30)
        self.fields['last_name'] = last_name
        email = forms.EmailField(label=_("Email"), max_length=75)
        self.fields['email'] = email
        username = forms.CharField(label=_("Username"), max_length=75)
        self.fields['username'] = username
        self.fields['password1'] = forms.CharField(label=_("Password"), max_length=32, widget=forms.PasswordInput)
        self.fields['password2'] = forms.CharField(label=_("Password confirmation"), max_length=32, widget=forms.PasswordInput)
        key_order = ['title', 'first_name', 'last_name', 'username', 'email',
            'password1', 'password2', 'institution', 'scientific_interests']
        if getattr(settings, 'USE_CAPTCHA', False):
            self.fields['captcha'] = ReCaptchaField()
            key_order.append('captcha')
        self.fields.keyOrder = key_order
        

    def is_aaf(self):
        try:
            return callable(getattr(self.user, 'is_aaf')) and self.user.is_aaf()
        except AttributeError:
            return False

    def clean_password1(self):
        if self.is_aaf():
            return ''
        password = self.cleaned_data.get('password1')
        if len(password) < settings.MIN_PASSWORD_LENGTH:
            raise ValidationError(_('Password must be at least %d characters long') % settings.MIN_PASSWORD_LENGTH)
        return password

    def clean_password2(self):
        if self.is_aaf():
            return ''
        password = self.cleaned_data.get('password2')
        if password != self.cleaned_data.get('password1'):
            raise ValidationError(_('Password confirmation does not match'))
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not self.is_aaf() and TaoUser.objects.filter(email=email).count() > 0:
            raise ValidationError(_('That email is already taken.'))
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not self.is_aaf() and TaoUser.objects.filter(username=username).count() > 0:
            raise ValidationError(_('That username is already taken.'))
        return username

    def save(self):  # what about transactions?
        UserModel = get_user_model()
        if self.is_aaf():
            self.user.title = self.cleaned_data['title']
            self.user.institution = self.cleaned_data['institution']
            self.user.scientific_interest = self.cleaned_data['scientific_interests']
            self.user.account_registration_status = UserModel.RS_PENDING
            self.user.save()
            user = self.user
        else:
            user = UserModel(username=self.clean_username())
            user.set_password(self.cleaned_data['password1'])
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.is_active = False
            user.title = self.cleaned_data['title']
            user.institution = self.cleaned_data.get('institution')
            user.scientific_interests = self.cleaned_data.get('scientific_interests')
            user.account_registration_status = UserModel.RS_NA
            user.save()
        return user


class RejectForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)


class SupportForm(forms.Form):
    subject = forms.CharField(max_length=80, validators=[RegexValidator(regex='[^ \t\n\r\f\v,]', message="This field cannot be blank")], required=True)
    message = forms.CharField(widget=forms.Textarea(), validators=[RegexValidator(regex='[^ \t\n\r\f\v,]', message="This field cannot be blank")], required=True)
