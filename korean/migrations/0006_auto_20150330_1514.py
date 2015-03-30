# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
        ('korean', '0005_teamreport_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamReportSubmit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.IntegerField()),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('season', models.ForeignKey(to='base.Season')),
                ('team', models.ForeignKey(to='korean.Team')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='teamreport',
            name='month',
        ),
        migrations.RemoveField(
            model_name='teamreport',
            name='season',
        ),
        migrations.RemoveField(
            model_name='teamreport',
            name='team',
        ),
        migrations.AddField(
            model_name='teamreport',
            name='report_submit',
            field=models.ForeignKey(default=1, to='korean.TeamReportSubmit'),
            preserve_default=False,
        ),
    ]
