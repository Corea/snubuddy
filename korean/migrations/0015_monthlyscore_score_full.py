# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('korean', '0014_monthlyscore_count_group_4'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyscore',
            name='score_full',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
