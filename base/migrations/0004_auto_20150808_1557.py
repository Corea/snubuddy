# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_userseason_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userseason',
            name='user_type',
            field=models.CharField(max_length=1, choices=[(b'A', '\uc6b4\uc601\uc9c4'), (b'K', '\ud55c\uad6d\uc778 \ubc84\ub514'), (b'F', '\uc678\uad6d\uc778 \ubc84\ub514')]),
        ),
    ]
