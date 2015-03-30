# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
        ('korean', '0003_personalreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.IntegerField()),
                ('grade', models.IntegerField(choices=[(0, 'A'), (1, 'B'), (2, 'C'), (3, 'D')])),
                ('season', models.ForeignKey(to='base.Season')),
                ('team', models.ForeignKey(to='korean.Team')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='groupevent',
            name='place_type',
            field=models.IntegerField(choices=[(0, '\uad50\ub0b4'), (1, '\ud559\uad50 \uadfc\ucc98'), (2, '\uc218\ub3c4\uad8c'), (3, '\uc218\ub3c4\uad8c \uc678'), (4, '\ud55c\uad6d\uc778 \ubaa8\uc784')]),
        ),
        migrations.AlterField(
            model_name='personalevent',
            name='place_type',
            field=models.IntegerField(choices=[(0, '\uad50\ub0b4'), (1, '\ud559\uad50 \uadfc\ucc98'), (2, '\uc218\ub3c4\uad8c'), (3, '\uc218\ub3c4\uad8c \uc678')]),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='leader_type',
            field=models.IntegerField(default=0, choices=[(0, ''), (1, '\uc870\uc7a5'), (2, '\ubd80\uc870\uc7a5')]),
        ),
    ]
