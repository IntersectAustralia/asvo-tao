import inspect
from django import forms
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction

from tao.models import UserProfile


class UserCreationForm(auth_forms.UserCreationForm):
    title = forms.CharField(label=_("Title"),
                            max_length=5)
    first_name = forms.CharField(label=_("First Name"),
                                    max_length=30)
    last_name = forms.CharField(label=_("Last Name"),
                                    max_length=30)
    institution = forms.CharField(label=_("Institution"), max_length=100)
    scientific_interests = forms.CharField(label=_("Scientific Interests"),
                                            max_length=500,
                                            widget=forms.Textarea(attrs={'rows':
                                            3}), required=False)
    email = forms.EmailField(label=_("Email"), max_length=75)


    class Meta:
        model = User
        fields = ('title', 'first_name', 'last_name', 'username', 'email',
        'password1', 'password2', 'institution', 'scientific_interests')


    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
# TODO internationalize
            raise ValidationError('Password must be at least 8 characters long')
        return password


    def save(self):  # what about transactions?
        user = super(auth_forms.UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # FIXME shouldn't have to do this ??
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        up = UserProfile(user=user)
        up.title = self.cleaned_data['title']
        up.institution = self.cleaned_data.get('institution')
        up.scientific_interests = self.cleaned_data.get('scientific_interests')
        up.save()

        return user
