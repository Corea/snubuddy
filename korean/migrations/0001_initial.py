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
            name='BuddyGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('season', models.ForeignKey(to='base.Season')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupAttend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('start_date', models.DateField()),
                ('place', models.CharField(max_length=256)),
                ('place_type', models.IntegerField(choices=[(0, b'\xea\xb5\x90\xeb\x82\xb4'), (1, b'\xed\x95\x99\xea\xb5\x90 \xea\xb7\xbc\xec\xb2\x98'), (2, b'\xec\x88\x98\xeb\x8f\x84\xea\xb6\x8c'), (3, b'\xec\x88\x98\xeb\x8f\x84\xea\xb6\x8c \xec\x99\xb8'), (4, b'\xed\x95\x9c\xea\xb5\xad\xec\x9d\xb8 \xeb\xaa\xa8\xec\x9e\x84')])),
                ('group', models.ForeignKey(to='korean.BuddyGroup')),
                ('staff', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonalEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('start_date', models.DateField()),
                ('place', models.CharField(max_length=256)),
                ('place_type', models.IntegerField(choices=[(0, b'\xea\xb5\x90\xeb\x82\xb4'), (1, b'\xed\x95\x99\xea\xb5\x90 \xea\xb7\xbc\xec\xb2\x98'), (2, b'\xec\x88\x98\xeb\x8f\x84\xea\xb6\x8c'), (3, b'\xec\x88\x98\xeb\x8f\x84\xea\xb6\x8c \xec\x99\xb8')])),
                ('photo', models.FileField(max_length=1024, upload_to=b'image/')),
                ('season', models.ForeignKey(to='base.Season')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('season', models.ForeignKey(to='base.Season')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamAttend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('start_date', models.DateField()),
                ('team', models.ForeignKey(to='korean.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('leader_type', models.IntegerField(default=0, choices=[(0, b''), (1, b'\xec\xa1\xb0\xec\x9e\xa5'), (2, b'\xeb\xb6\x80\xec\xa1\xb0\xec\x9e\xa5')])),
                ('group', models.ForeignKey(to='korean.BuddyGroup')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_leader', models.BooleanField(default=False)),
                ('team', models.ForeignKey(to='korean.Team')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='teamattend',
            name='event',
            field=models.ForeignKey(to='korean.TeamEvent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='teamattend',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupattend',
            name='event',
            field=models.ForeignKey(to='korean.GroupEvent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupattend',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
