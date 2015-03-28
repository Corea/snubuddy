# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
        ('korean', '0002_auto_20150328_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.IntegerField()),
                ('question1', models.TextField(blank=True)),
                ('question2', models.TextField(blank=True)),
                ('question3', models.TextField(blank=True)),
                ('question4', models.TextField(blank=True)),
                ('question5', models.TextField(blank=True)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('season', models.ForeignKey(to='base.Season')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
