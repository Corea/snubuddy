# -*- coding: utf-8 -*-

from datetime import datetime

from itertools import groupby
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

from base.templatetags.filters import is_team_leader, is_group_leader

from application.models import ApplicationForeigner
from korean.models import (
    PersonalEvent, GroupEvent, GroupAttend, TeamEvent, TeamAttend
)
from base.decorators import group_required

from base import queries as base_queries
from matching import queries as matching_queries
from korean import queries as korean_queries
from korean.forms import PersonalEventForm, GroupEventForm, TeamEventForm


@login_required
@group_required('Korean')
def evaluation_status(request):
    personal_events = PersonalEvent.objects.filter(
        user=request.user,
        season=base_queries.get_this_season()
    ).order_by('start_date')

    return render(request, 'evaluation/status.html', {
        'personal_events': personal_events
    })


@login_required
@group_required('Korean')
def add_personal_activity(request):
    # TODO: Make restriction by evaluation.

    form = PersonalEventForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)
        event.user = request.user
        event.season = base_queries.get_this_season()
        event.save()
        return redirect(evaluation_list)

    return render(request, 'evaluation/add_personal_activity.html', {
        'form': form,
    })


@login_required
@group_required('Korean')
def remove_personal_activity(request, event_id):
    event = get_object_or_404(PersonalEvent, id=event_id)
    # TODO: Make restriction by evaluation.

    if event.user == request.user:
        event.delete()

    return redirect(evaluation_status)


@login_required
@group_required('Korean')
def add_group_activity(request):
    if not is_group_leader(request.user):
        return redirect(evaluation_list)

    form = GroupEventForm(request.POST or None, request.FILES or None)
    return render(request, 'evaluation/add_group_activity.html', {
        'form': form,
    })


@login_required
@group_required('Korean')
def add_team_activity(request):
    if not is_team_leader(request.user):
        return redirect(evaluation_list)
    form = TeamEventForm(request.POST or None)
    koreans = map(lambda x: (korean_queries.get_team_name_by_user(x), x),
                  korean_queries.get_korean_list())
    koreans = dict((k, sorted([v for (_, v) in g],
                              key=lambda x: x.profile.korean_name)) for k, g in
                   groupby(sorted(koreans), key=lambda (k, v): k))

    return render(request, 'evaluation/add_team_activity.html', {
        'form': form,
        'koreans': koreans,
    })


@login_required
@group_required('Admin')
def korean_list(request):
    users = korean_queries.get_korean_list('birth')

    infos = []
    for user in users:
        exist = matching_queries.has_matching(user)
        userteam = korean_queries.get_userteam_by_user(user)
        usergroup = korean_queries.get_usergroup_by_user(user)
        infos.append([user, exist, userteam, usergroup])

    return render(request, 'korean/korean_list.html', {
        'infos': infos,
        'teams': korean_queries.get_team_list(),
        'groups': korean_queries.get_group_list()
    })


@login_required
@group_required('Admin')
def full_list(request):
    season = base_queries.get_this_season()
    groups = korean_queries.get_group_list()
    infos = []
    for group in groups:
        usergroups = korean_queries.get_usergroups_by_group(group)
        inner_info = [[x, [[y, ApplicationForeigner.objects.get(user=y,
                                                                season=season
                            )] for y in matching_queries.get_personal_buddies_by_user(x.user)]]
                      for x in usergroups]
        infos.append([group, inner_info])

    return render(request, 'korean/full_list.html', {
        'infos': infos
    })


@login_required
@group_required('Admin')
def make_member(request):
    if request.method != 'POST':
        return redirect(korean_list)

    checked_ids = map(int, request.POST.getlist('checked_ids'))

    try:
        team = request.POST.get('team', None)
        team_leader = request.POST.get('team_leader', None)
        group = request.POST.get('group', None)
        group_leader = request.POST.get('group_leader', None)

        if team or team_leader:
            # Team
            if team is not None:
                team = int(team)
                team = korean_queries.get_team(team) if team != 0 else 0

            for user_id in checked_ids:
                user = base_queries.get_user(user_id)

                if team_leader:
                    korean_queries.make_team_leader(user)
                else:
                    korean_queries.make_team_member(user, team)
        elif group or group_leader:
            # Group
            if group is not None:
                group = int(group)
                group = korean_queries.get_group(group)

            for user_id in checked_ids:
                user = base_queries.get_user(user_id)

                if group_leader:
                    korean_queries.make_group_leader(user, group_leader)
                else:
                    korean_queries.make_group_member(user, group)
    except:
        pass

    return redirect(korean_list)
