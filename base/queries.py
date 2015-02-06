# -*- coding: utf-8 -*-

from base.models import Season


def get_this_season():
    return Season.objects.filter(is_this_season=True)[0]
