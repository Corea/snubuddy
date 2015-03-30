# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.contrib.auth.models import User, Group

from korean.models import (
    Team, UserTeam, BuddyGroup, UserGroup,
    PersonalReport, TeamReport, GroupReport
)
from base.queries import get_this_season


def get_korean_list(sort_option=''):
    sort_key = (lambda x: x.profile.korean_name)
    if sort_option == 'birth':
        sort_key = (lambda x: (x.profile.birth.month, x.profile.birth.day))

    users = Group.objects.get(name='Korean').user_set.all()
    users = sorted(users, key=sort_key)
    return users


# Team
def get_userteam_by_user(user):
    try:
        return UserTeam.objects.get(
            user=user,
            team__season=get_this_season())
    except:
        return None


def get_team_by_user(user):
    userteam = get_userteam_by_user(user)
    return userteam.team if userteam else None


def get_team_name_by_user(user):
    team = get_team_by_user(user)
    return team.name if team else ''


def get_member_by_team(team):
    return sorted(map(lambda x: x.user,
                      UserTeam.objects.filter(team=team)),
                  key=lambda x: x.profile.korean_name)


def make_team_member(user, team):
    UserTeam.objects.filter(
        user=user,
        team__season=get_this_season()).delete()

    if team != 0:
        UserTeam.objects.create(user=user, team=team)


def make_team_leader(user):
    userteam = get_userteam_by_user(user)
    if userteam is not None:
        userteam.is_leader = True
        userteam.save()


# Group
def get_usergroup_by_user(user):
    try:
        return UserGroup.objects.get(
            user=user,
            group__season=get_this_season())
    except:
        return None


def get_buddygroup_by_user(user):
    usergroup = get_usergroup_by_user(user)
    return usergroup.group if usergroup is not None else None


def get_member_by_buddygroup(group):
    return map(lambda x: x.user, UserGroup.objects.filter(group=group))


def make_group_member(user, group):
    UserGroup.objects.filter(
        user=user,
        group__season=get_this_season()).delete()

    UserGroup.objects.create(user=user, group=group)


def make_group_leader(user, leader_type):
    usergroup = get_usergroup_by_user(user)
    if usergroup is not None:
        usergroup.leader_type = leader_type
        usergroup.save()


# Report
def get_target_month():
    return (datetime.now().date() - timedelta(days=14)).month


def exist_personal_report(user, month):
    return PersonalReport.objects.filter(
        user=user, season=get_this_season(), month=month).exists()


def exist_group_report(user, month):
    return GroupReport.objects.filter(
        user=user, season=get_this_season(), month=month).exists()


def exist_team_report(team, month):
    result = TeamReport.objects.filter(
        team=team, season=get_this_season(), month=month).exists()

    if month == 2 or month == 8:
        result |= TeamReport.objects.filter(
            team=team, season=get_this_season(), month=month+1).exists()

    return result
