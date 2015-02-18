# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group

from korean.models import Team, UserTeam
from base import queries as base_queries


def get_korean_list(sorted_birth=False):
    users = Group.objects.get(name='Korean').user_set.all()
    if sorted_birth:
        users = sorted(users, 
            key=lambda x: (x.profile.birth.month, x.profile.birth.day))

    return users


def get_team(team_id):
    return Team.objects.get(id=team_id)


def get_team_list():
    return Team.objects.filter(season=base_queries.get_this_season())


def get_userteam_by_user(user):
    try:
        return UserTeam.objects.get(
            user=user,
            team__season=base_queries.get_this_season())
    except:
        return None


def get_team_by_user(user):
    userteam = get_userteam_by_user(user)
    return userteam.team if userteam else None


def get_team_name_by_user(user):
    team = get_team_by_user(user)
    return team.name if team else ''


def make_team_member(user, team):
    UserTeam.objects.filter(
        user=user,
        team__season=base_queries.get_this_season()).delete()

    if team != 0:
        UserTeam.objects.create(user=user, team=team)


def make_team_leader(user):
    userteam = get_userteam_by_user(user)
    if userteam is not None:
        userteam.is_leader = True
        userteam.save()
