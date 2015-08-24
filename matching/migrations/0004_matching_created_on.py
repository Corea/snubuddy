# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0003_auto_20150217_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='matching',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 8, 15, 57, 7, 904471), auto_now_add=True),
            preserve_default=False,
        ),
    ]
