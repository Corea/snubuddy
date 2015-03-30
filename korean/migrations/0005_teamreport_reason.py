# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('korean', '0004_auto_20150329_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamreport',
            name='reason',
            field=models.CharField(default='', max_length=512, blank=True),
            preserve_default=False,
        ),
    ]
