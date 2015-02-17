# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0002_auto_20150206_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matching',
            name='gender_preference',
            field=models.CharField(max_length=1, null=True, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'B', b'Both')]),
        ),
    ]
