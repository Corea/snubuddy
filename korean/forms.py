# -*- coding: utf-8 -*-

from datetime import date

from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminFileWidget

from korean.models import PersonalEvent, GroupEvent, TeamEvent


class PersonalEventForm(ModelForm):
    class Meta:
        model = PersonalEvent
        fields = ('title', 'start_date', 'place', 'place_type', 'photo')
        labels = {
            'title': u'Particulars',
            'start_date': u'Date',
            'place': u'Remarks',
            'place_type': u'Category',
        }
        help_texts = {
            'start_date': u'시작 날짜만 기입, ex) 2015-03-03',
        }

    def is_valid(self):
        valid = super(PersonalEventForm, self).is_valid()

        if self.cleaned_data['start_date'].date() > date.today():
            self.add_error('start_date', 'Please make sure the date.')
            valid = False

        if not valid:
            return valid

        return True


class GroupEventForm(ModelForm):
    class Meta:
        model = GroupEvent
        fields = ('title', 'start_date', 'place', 'place_type')
        labels = {
            'title': u'Particulars',
            'start_date': u'Date',
            'place': u'Remarks',
            'place_type': u'Category',
        }
        help_texts = {
            'start_date': u'시작 날짜만 기입, ex) 2015-03-03',
        }


class TeamEventForm(ModelForm):
    class Meta:
        model = GroupEvent
        fields = ('title', 'start_date')
        labels = {
            'title': u'Particulars',
            'start_date': u'Date',
        }
        help_texts = {
            'start_date': u'시작 날짜만 기입, ex) 2015-03-03',
        }
