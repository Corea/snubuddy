# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group

from base.models import Season, Country, Language


def get_this_season():
    return Season.objects.filter(is_this_season=True)[0]


def get_user(user_id):
    return User.objects.get(id=user_id)


def is_korean(user):
    return user.groups.filter(name='Korean').exists()


def get_country(country_id):
    return Country.objects.get(id=country_id)


def get_language(language_id):
    return Language.objects.get(id=language_id)
