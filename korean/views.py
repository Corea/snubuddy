# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

from base.decorators import group_required

from base import queries as base_queries
from matching import queries as matching_queries
from korean import queries as korean_queries


@login_required
def index(request):
    return render(request, 'korean/index.html', {})


@login_required
@group_required('Admin')
def korean_list(request):
    users = korean_queries.get_korean_list(True)

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

    # return HttpResponse(map(lambda x: x + " ", request.POST.getlist('checked_ids')))

