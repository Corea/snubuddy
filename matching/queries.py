# -*- coding: utf-8 -*-

from matching.models import Matching, MatchingConnection, MatchingLanguage

from base import queries as base_queries


def get_personal_buddies(matching):
    return map(lambda x: x.foreign_matching,
               MatchingConnection.objects.filter(korean_matching=matching))


def get_korean_matching_list():
    matching_list = Matching.objects.filter(
        user__groups__name='Korean',
        season=base_queries.get_this_season()).order_by('id')

    return matching_list


def count_matched_buddies(matching):
    return MatchingConnection.objects.filter(korean_matching=matching).count()


def delete_matching(matching):
    # Remove Language
    MatchingLanguage.objects.filter(matching=matching).delete()

    # If Korean Buddy?
    matching_connections = MatchingConnection.objects.filter(
        korean_matching=matching)
    for connection in matching_connections:
        delete_matching(connection.foreign_matching)

    # If Foreigner Buddy?
    MatchingConnection.objects.filter(foreign_matching=matching).delete()
    matching.delete()


def delete_matching_by_user(user):
    matching_list = Matching.objects.filter(
        user=user, season=base_queries.get_this_season())

    for matching in matching_list:
        delete_matching(matching)


def get_matching_by_user(user):
    try:
        return Matching.objects.get(user=user,
                                    season=base_queries.get_this_season())
    except:
        return None


def has_matching(user):
    return get_matching_by_user(user) is not None


def get_personal_buddies_by_user(user):
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
