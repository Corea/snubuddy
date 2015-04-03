# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('korean', '0009_personalevent_is_language_exchange'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupevent',
            name='is_lunch',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
