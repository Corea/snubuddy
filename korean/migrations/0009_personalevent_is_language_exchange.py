# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('korean', '0008_auto_20150330_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalevent',
            name='is_language_exchange',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
