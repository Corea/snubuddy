# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_applicationforeigner_returning'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationforeigner',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 10, 18, 45, 8, 431856), auto_now_add=True),
            preserve_default=False,
        ),
    ]
