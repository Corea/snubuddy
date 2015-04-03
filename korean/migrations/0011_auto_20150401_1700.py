# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('korean', '0010_groupevent_is_lunch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamattend',
            name='score',
            field=models.FloatField(),
        ),
    ]
