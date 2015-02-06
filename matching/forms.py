# -*- coding: utf-8 -*-

from django.forms import ModelForm

from matching.models import Matching


class MatchingKoreanForm(ModelForm):
    class Meta:
        model = Matching
        exclude = ('user', 'season')
        labels = {}
        help_texts = {}


class MatchingForeignerForm(ModelForm):
    class Meta:
        model = Matching
        exclude = ('user', 'season', 'gender_preference', 'max_buddy_number')
        labels = {}
        help_texts = {}
