# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('korean', '0013_monthlyscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyscore',
            name='count_group_4',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
