# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from base.models import Language
from matching.models import Matching


class LanguageWidget(forms.Widget):
    template_name = 'widget/language_list.html'

    def render(self, name, value, attrs=None):
        context = {
            'language_list': Language.objects.all()
        }
        return mark_safe(render_to_string(self.template_name, context))


class MatchingKoreanForm(ModelForm):
    language = forms.Field(widget=LanguageWidget, required=False)

    class Meta:
        model = Matching
        exclude = ('user', 'season')
        labels = {}
        help_texts = {}

    def is_valid(self):
        valid = super(MatchingKoreanForm, self).is_valid()

        try:
            languages = self.data.getlist('language[]')
            print languages
            for item in languages:
                if Language.objects.filter(id=int(item)).count() != 1:
                    raise

            language_levels = map(int, self.data.getlist('language_level[]'))
            if max(language_levels) > 4 or min(language_levels) < 1:
                raise

            if len(languages) != len(language_levels):
                raise
        except:
            self._errors['language'] = ['Something wrong with this field']
            return False

        return valid



class MatchingForeignerForm(ModelForm):
    language = forms.Field(widget=LanguageWidget, required=False)

    class Meta:
        model = Matching
        exclude = ('user', 'season', 'gender_preference', 'max_buddy_number')
        labels = {}
        help_texts = {}

    def is_valid(self):
        valid = super(MatchingForeignerForm, self).is_valid()

        try:
            languages = self.data.getlist('language[]')
            print languages
            for item in languages:
                if Language.objects.filter(id=int(item)).count() != 1:
                    raise

            language_levels = map(int, self.data.getlist('language_level[]'))
            if max(language_levels) > 4 or min(language_levels) < 1:
                raise

            if len(languages) != len(language_levels):
                raise
        except:
            self._errors['language'] = ['Something wrong with this field']
            return False

        return valid

