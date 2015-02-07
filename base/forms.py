# -*- coding: utf-8 -*-

from django import forms 
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from base.models import Country, Language, UserProfile


class RegistrationForm(forms.Form):
    required_css_class = 'required'

    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label=_("Username"),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")},
                                required=True)
    first_name = forms.CharField(max_length=64,
                                 label=_("First Name"),
                                 required=True)
    last_name = forms.CharField(max_length=64,
                                 label=_("Last Name"),
                                 required=True)
    email = forms.EmailField(label=_("E-mail"), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"),
                                required=True)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (again)"),
                                required=True)
    korean_name = forms.CharField(max_length=64,
                                  label=_("Korean Name (Optional)"),
                                  required=False)
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES,
                               required=True)
    birth = forms.DateField(required=True)
    country = forms.ModelChoiceField(queryset=Country.objects.all())

    def clean(self):
        if 'username' in self.cleaned_data:
            existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
            if existing.exists():
                raise forms.ValidationError(_("A user with that username already exists."))

        if 'email' in self.cleaned_data:
            existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
            if existing.exists():
                raise forms.ValidationError(_("A user with that email already exists."))

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))

        return self.cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            korean_name=self.cleaned_data['korean_name'],
            gender=self.cleaned_data['gender'],
            birth=self.cleaned_data['birth'],
            country=self.cleaned_data['country']
        )
        profile.save()


class SettingsForm(forms.Form):
    user = None
    first_name = forms.CharField(max_length=64,
                                 label=_("First Name"),
                                 required=True)
    last_name = forms.CharField(max_length=64,
                                 label=_("Last Name"),
                                 required=True)
    email = forms.EmailField(label=_("E-mail"), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password Change"),
                                required=False)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (again)"),
                                required=False)
    korean_name = forms.CharField(max_length=64,
                                  label=_("Korean Name (Optional)"),
                                  required=False)
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES,
                               required=True)
    birth = forms.DateField(required=True)
    country = forms.ModelChoiceField(queryset=Country.objects.all())

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u'비밀 번호가 일치하지 않습니다.')

        if 'email' in self.cleaned_data:
            existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
            if existing.exists() and existing[0] != self.user:
                raise forms.ValidationError(_("A user with that email already exists."))

        return self.cleaned_data

    def save(self, user):
        pw = self.cleaned_data['password1']
        if len(pw) > 0:
            user.set_password(pw)
            user.save()

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        profile = user.profile
        profile.korean_name = self.cleaned_data['korean_name']
        profile.gender = self.cleaned_data['gender']
        profile.birth = self.cleaned_data['birth']
        profile.country = self.cleaned_data['country']
        profile.save()
