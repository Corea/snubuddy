# -*- coding: utf-8 -*-

from base import queries as base_queries
from matching.models import Matching


def has_matching(user):
    return Matching.objects.filter(
        user=user, 
        season=base_queries.get_this_season()
    ).exists()
