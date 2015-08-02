# -*- coding: utf-8 -*-

from datetime import date

from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.admin.widgets import AdminFileWidget

from django.contrib.auth.models import User
from korean.models import (
    UserGroup, PersonalEvent, GroupEvent, TeamEvent,
    PersonalReport
)


class PersonalEventForm(ModelForm):
    class Meta:
        model = PersonalEvent
        fields = ('title', 'start_date', 'place', 'place_type',
                  'photo', 'is_language_exchange')
        labels = {
            'title': u'Title',
            'start_date': u'Date',
            'place': u'Place',
            'place_type': u'Category',
            'is_language_exchange': u'Language Exchange?'
        }
        help_texts = {
            'start_date': u'시작 날짜만 기입, ex) 2015-03-03',
        }

    def is_valid(self):
        valid = super(PersonalEventForm, self).is_valid()

        if 'start_date' in self.cleaned_data and \
                self.cleaned_data['start_date'] > date.today():
            self.add_error('start_date', 'Please make sure the date.')
            valid = False

        return valid


class GroupEventForm(ModelForm):
    def __init__(self, group, *args, **kwargs):
        super(GroupEventForm, self).__init__(*args, **kwargs)
        self.fields['host'].queryset = User.objects.filter(
            id__in=UserGroup.objects.filter(group=group).values('user'))
        self.fields['host'].label_from_instance = \
            lambda obj: obj.profile.korean_name

    class Meta:
        model = GroupEvent
        fields = ('title', 'start_date', 'host', 'place',
                  'place_type', 'is_lunch')
        labels = {
            'title': u'Title',
            'host': u'Host',
            'start_date': u'Date',
            'place': u'Place',
            'place_type': u'Category',
            'is_lunch': u'Lunch Gathering?', 
        }
        help_texts = {
            'start_date': u'시작 날짜만 기입, ex) 2015-03-03',
        }

    def is_valid(self):
        valid = super(GroupEventForm, self).is_valid()

        if 'start_date' in self.cleaned_data and \
                self.cleaned_data['start_date'] > date.today():
            self.add_error('start_date', 'Please make sure the date.')
            valid = False

        return valid


class TeamEventForm(ModelForm):
    class Meta:
        model = TeamEvent
        fields = ('title', 'start_date')
        labels = {
            'title': u'Title',
            'start_date': u'Date',
        }
        help_texts = {
            'start_date': u'시작 날짜만 기입, ex) 2015-03-03',
        }

    def is_valid(self):
        valid = super(TeamEventForm, self).is_valid()

        if 'start_date' in self.cleaned_data and \
                self.cleaned_data['start_date'] > date.today():
            self.add_error('start_date', 'Please make sure the date.')
            valid = False

        return valid


class PersonalReportForm(ModelForm):
    class Meta:
        model = PersonalReport
        exclude = ('user', 'season', 'month', 'created_datetime')
        labels = {
            'question1': u'1. 이번 달 자신의 버디와 만난 횟수는? (조모임 활동 제외)',
            'question2': u'2. 일주일 동안 버디와 함께 보내는 시간은 평균 몇시간입니까? (조모임 활동 제외)',
            'question3': u'3. SNU Buddy 활동에 있는 애로사항을 이야기해 주세요.',
            'question4': u'4. SNU Buddy 활동에 대한 건의사항이 있습니까?',
            'question5': u'5. 다음 달 활동에 임하는 마음가짐을 이야기해 주세요.',
        }
        widgets = {
            'question1': Textarea(attrs={'rows': 3}),
            'question2': Textarea(attrs={'rows': 3}),
            'question3': Textarea(attrs={'rows': 3}),
            'question4': Textarea(attrs={'rows': 3}),
            'question5': Textarea(attrs={'rows': 3}),
        }
