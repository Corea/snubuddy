# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='matching',
            name='gender_preference',
            field=models.CharField(max_length=1, null=True, choices=[(b'M', b'Male'), (b'F', b'Female')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='matching',
            name='max_buddy_number',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
