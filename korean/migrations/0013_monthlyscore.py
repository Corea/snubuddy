# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
        ('korean', '0012_auto_20150407_0948'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.IntegerField()),
                ('count_personal_0', models.IntegerField(default=0)),
                ('count_personal_1', models.IntegerField(default=0)),
                ('count_personal_2', models.IntegerField(default=0)),
                ('count_personal_3', models.IntegerField(default=0)),
                ('count_group_0', models.IntegerField(default=0)),
                ('count_group_1', models.IntegerField(default=0)),
                ('count_group_2', models.IntegerField(default=0)),
                ('count_group_3', models.IntegerField(default=0)),
                ('score_personal', models.FloatField(default=0)),
                ('score_group', models.FloatField(default=0)),
                ('score_team', models.FloatField(default=0)),
                ('season', models.ForeignKey(to='base.Season')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
