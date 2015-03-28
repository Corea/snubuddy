# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('korean', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupevent',
            old_name='staff',
            new_name='host',
        ),
    ]
