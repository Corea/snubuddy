# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('korean', '0007_auto_20150330_2113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teamevaluation',
            old_name='report_submit',
            new_name='report',
        ),
    ]
