# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_applicationforeigner_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationforeigner',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
    ]
