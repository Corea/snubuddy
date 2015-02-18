# -*- coding: utf-8 -*-

from matching.models import Matching, MatchingConnection

from base import queries as base_queries


def get_matching_by_user(user):
    try:
        return Matching.objects.get(user=user,
            season=base_queries.get_this_season())
    except:
        return None


def has_matching(user):
    return get_matching_by_user(user) is not None


def get_personal_buddies(user):
    if base_queries.is_korean(user):
        korean_matching = get_matching_by_user(user)
        matching_connections = MatchingConnection.objects.filter(
            korean_matching=korean_matching)
        return map(lambda x: x.foreign_matching.user, matching_connections)
    else:
        foreign_matching = get_matching_by_user(user)
        matching_connections = MatchingConnection.objects.filter(
            foreign_matching=foreign_matching)
        return map(lambda x: x.korean_matching.user, matching_connections)
