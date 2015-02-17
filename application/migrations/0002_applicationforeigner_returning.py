# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationforeigner',
            name='returning',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
