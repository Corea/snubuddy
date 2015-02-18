# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group

from base.models import Season


def get_this_season():
    return Season.objects.filter(is_this_season=True)[0]


def get_user(user_id):
    return User.objects.get(id=user_id)


def is_korean(user):
    return user.groups.filter(name='Korean').exists()
