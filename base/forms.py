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
    email = forms.EmailField(label=_("E-mail"), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"),
                                required=True)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (again)"),
                                required=True)
    korean_name = forms.CharField(max_length=64)
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES,
                               required=True)
    birth = forms.DateField(required=True)
    country = forms.ModelChoiceField(queryset=Country.objects.all())

    def clean(self):
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))

        return self.cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']

        user = User.objects.create_user(username, email, password)
        profile = UserProfile.objects.create(
            user=user,
            korean_name=self.cleaned_data['korean_name'],
            gender=self.cleaned_data['gender'],
            birth=self.cleaned_data['birth'],
            country=self.cleaned_data['country']
        )
        profile.save()


class SettingsForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                required=False, label=u'비밀번호 변경')
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                required=False, label=u'비밀번호 (확인)')

    name = forms.CharField(label=u'한글 이름', max_length=30)

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u'비밀 번호가 일치하지 않습니다.')
        return self.cleaned_data

    def save(self, user):
        pw = self.cleaned_data['password1']
        if len(pw) > 0:
            user.set_password(pw)
            user.save()
        user.first_name = self.cleaned_data['name']
        user.save()
