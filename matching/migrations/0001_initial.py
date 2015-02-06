# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Matching',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('major', models.CharField(max_length=64)),
                ('hobby', models.CharField(max_length=128)),
                ('interest', models.CharField(max_length=128)),
                ('self_introduction', models.TextField()),
                ('comment', models.TextField()),
                ('season', models.ForeignKey(to='base.Season')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MatchingConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('foreign_matching', models.ForeignKey(related_name=b'foreign', to='matching.Matching')),
                ('korean_matching', models.ForeignKey(related_name=b'korean', to='matching.Matching')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MatchingLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField()),
                ('language', models.ForeignKey(to='base.Language')),
                ('matching', models.ForeignKey(to='matching.Matching')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
