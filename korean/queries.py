# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group

from korean.models import Team, UserTeam, BuddyGroup, UserGroup
from base import queries as base_queries


def get_korean_list(sort_option=''):
    sort_key = (lambda x: x.profile.korean_name)
    if sort_option == 'birth':
        sort_key = (lambda x: (x.profile.birth.month, x.profile.birth.day))

    users = Group.objects.get(name='Korean').user_set.all()
    users = sorted(users, key=sort_key)
    return users


# Team
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


# Group
def get_group(group_id):
    return BuddyGroup.objects.get(id=group_id)


def get_group_list():
    return BuddyGroup.objects.filter(season=base_queries.get_this_season())


def get_usergroups_by_group(group):
    return UserGroup.objects.filter(group=group)


def get_usergroup_by_user(user):
    try:
        return UserGroup.objects.get(
            user=user,
            group__season=base_queries.get_this_season())
    except:
        return None


def make_group_member(user, group):
    UserGroup.objects.filter(
        user=user,
        group__season=base_queries.get_this_season()).delete()

    UserGroup.objects.create(user=user, group=group)


def make_group_leader(user, leader_type):
    usergroup = get_usergroup_by_user(user)
    if usergroup is not None:
        usergroup.leader_type = leader_type
        usergroup.save()
