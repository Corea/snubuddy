# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_userseason'),
    ]

    operations = [
        migrations.AddField(
            model_name='userseason',
            name='user_type',
            field=models.CharField(default='', max_length=1, choices=[(b'A', b'Admin'), (b'K', b'Korean'), (b'F', b'Foreigner')]),
            preserve_default=False,
        ),
    ]
