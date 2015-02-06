# -*- coding: utf-8 -*-

from django.forms import ModelForm

from application.models import ApplicationForeigner


class ApplicationForeignerForm(ModelForm):
    class Meta:
        model = ApplicationForeigner
        exclude = ('user', 'season')
        labels = {
            'snu_id': 'SNU Member No.',
            'fb_name': 'Facebook Name',
            'fb_email': 'Facebook E-Mail'
        }
        help_texts = {
            'fb_name': 'We will send out Facebook invitations for the SNU Buddy group.',
        }
