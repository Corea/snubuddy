# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('korean', '0011_auto_20150401_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupevent',
            name='is_confirm',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personalevent',
            name='is_confirm',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
