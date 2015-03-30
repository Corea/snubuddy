# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
        ('korean', '0006_auto_20150330_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupEvaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score1', models.IntegerField()),
                ('score2', models.IntegerField()),
                ('reason', models.CharField(max_length=512, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.IntegerField()),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(to='korean.BuddyGroup')),
                ('season', models.ForeignKey(to='base.Season')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel('TeamReport', 'TeamEvaluation'),
        migrations.RenameModel('TeamReportSubmit', 'TeamReport'),
        migrations.AddField(
            model_name='groupevaluation',
            name='report',
            field=models.ForeignKey(to='korean.GroupReport'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupevaluation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
