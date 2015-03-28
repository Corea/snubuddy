# -*- coding: utf-8 -*-

from itertools import groupby
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

from base.templatetags.filters import is_team_leader, is_group_leader

from application.models import ApplicationForeigner
from korean.models import (
    Team, UserTeam, BuddyGroup, UserGroup,
    PersonalEvent, GroupEvent, GroupAttend, TeamEvent, TeamAttend,
    PersonalReport
)
from base.decorators import group_required

from base.queries import get_this_season, get_user
from matching.queries import get_personal_buddies_by_user, has_matching
from korean.forms import (
    PersonalEventForm, GroupEventForm, TeamEventForm, PersonalReportForm
)

from korean import queries as korean_queries


@login_required
@group_required('Korean')
def evaluation_status(request):
    personal_events = PersonalEvent.objects.filter(
        user=request.user,
        season=get_this_season()
    ).order_by('start_date')

    team_attends = TeamAttend.objects.filter(
        user=request.user,
        event__team__season=get_this_season()).order_by('event__start_date')

    group_attended_events = map(lambda x: x.event, GroupAttend.objects.filter(
        user=request.user,
        event__group__season=get_this_season()).order_by('event__start_date'))

    attended_events = map(lambda x: ('Personal', x), list(personal_events)) + \
        map(lambda x: ('Group', x), list(group_attended_events)) + \
        map(lambda x: ('Team', x), list(team_attends))
    attended_events = sorted(attended_events,
        key=lambda x: x[1].start_date if x[0] != 'Team' else x[1].event.start_date)

    reports = map(lambda x: ('Personal', x),
        PersonalReport.objects.filter(
            user=request.user, season=get_this_season()))
    team_events = []
    group_events = []

    if is_team_leader(request.user):
        team_events = TeamEvent.objects.filter(
            team=korean_queries.get_team_by_user(request.user)
        ).order_by('start_date')

    if is_group_leader(request.user):
        group_events = GroupEvent.objects.filter(
            group=korean_queries.get_buddygroup_by_user(request.user)
        ).order_by('start_date')

    return render(request, 'evaluation/status.html', {
        'attended_events': attended_events,
        'personal_events': personal_events,
        'team_events': team_events,
        'group_events': group_events,
        'reports': reports,
    })


@login_required
@group_required('Korean')
def add_personal_activity(request):
    # TODO: Make restriction by evaluation.

    form = PersonalEventForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)
        event.user = request.user
        event.season = get_this_season()
        event.save()
        return redirect(evaluation_status)

    return render(request, 'evaluation/add_personal_activity.html', {
        'form': form,
    })


# ACTIVITY PART
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
        return redirect(evaluation_status)
    group = korean_queries.get_buddygroup_by_user(request.user)
    members = map(lambda x: [x, False],
                  sorted(korean_queries.get_member_by_buddygroup(group),
                         key=lambda x: x.profile.korean_name))
    checked_ids = map(int, request.POST.getlist('checked_ids'))

    for member in members:
        if member[0].id in checked_ids:
            member[1] = True

    form = GroupEventForm(group, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)
        event.group = group
        event.save()

        for (user, check) in members:
            if check:
                attend = GroupAttend.objects.create(event=event, user=user)
                attend.save()

        return redirect(evaluation_status)

    return render(request, 'evaluation/add_group_activity.html', {
        'form': form,
        'members': members
    })


@login_required
@group_required('Korean')
def modify_group_activity(request, event_id):
    if not is_group_leader(request.user):
        return redirect(evaluation_status)

    event = get_object_or_404(GroupEvent, id=event_id)
    if event.group != korean_queries.get_buddygroup_by_user(request.user):
        return redirect(evaluation_status)

    group = korean_queries.get_buddygroup_by_user(request.user)
    members = map(lambda x: [x, False],
                  sorted(korean_queries.get_member_by_buddygroup(group),
                         key=lambda x: x.profile.korean_name))
    checked_ids = map(int, request.POST.getlist('checked_ids'))

    for member in members:
        user = member[0]
        member[1] = GroupAttend.objects.filter(
            event=event, user=user).exists()

        if user.id in checked_ids:
            member[1] = True

    form = GroupEventForm(group, request.POST or None, instance=event)
    if request.method == 'POST' and form.is_valid():
        GroupAttend.objects.filter(event=event).delete()
        event = form.save()

        for (user, check) in members:
            if check:
                attend = GroupAttend.objects.create(event=event, user=user)
                attend.save()

        return redirect(evaluation_status)

    return render(request, 'evaluation/add_group_activity.html', {
        'form': form,
        'members': members
    })


@login_required
@group_required('Korean')
def remove_group_activity(request, event_id):
    if not is_group_leader(request.user):
        return redirect(evaluation_status)
    event = get_object_or_404(GroupEvent, id=event_id)
    # TODO: Make restriction by evaluation.

    if event.group == korean_queries.get_buddygroup_by_user(request.user):
        GroupAttend.objects.filter(event=event).delete()
        event.delete()

    return redirect(evaluation_status)


@login_required
@group_required('Korean')
def add_team_activity(request):
    if not is_team_leader(request.user):
        return redirect(evaluation_status)
    form = TeamEventForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)
        event.team = korean_queries.get_team_by_user(request.user)
        event.save()

        for user in korean_queries.get_korean_list():
            score = int(request.POST.get('score_' + str(user.id), 0))
            if score == 0:
                continue

            attend = TeamAttend.objects.create(
                event=event, user=user, score=score)
            attend.save()

        return redirect(evaluation_status)

    koreans = {}
    for user in korean_queries.get_korean_list():
        team_name = korean_queries.get_team_name_by_user(user)
        if team_name == '':
            team_name = u'회장단'

        if team_name not in koreans:
            koreans[team_name] = []
        score = request.POST.get('score_' + str(user.id), 0)
        koreans[team_name].append((user, score))

    for value in koreans.itervalues():
        value = sorted(value, key=lambda x: x[0].profile.korean_name)
    koreans = reversed(sorted(koreans.iteritems()))

    return render(request, 'evaluation/add_team_activity.html', {
        'form': form,
        'koreans': koreans,
    })


@login_required
@group_required('Korean')
def modify_team_activity(request, event_id):
    if not is_team_leader(request.user):
        return redirect(evaluation_status)

    event = get_object_or_404(TeamEvent, id=event_id)
    if event.team != korean_queries.get_team_by_user(request.user):
        return redirect(evaluation_status)

    form = TeamEventForm(request.POST or None, instance=event)
    if request.method == 'POST' and form.is_valid():
        TeamAttend.objects.filter(event=event).delete()
        event = form.save()

        for user in korean_queries.get_korean_list():
            score = int(request.POST.get('score_' + str(user.id), 0))
            if score == 0:
                continue

            attend = TeamAttend.objects.create(
                event=event, user=user, score=score)
            attend.save()

        return redirect(evaluation_status)

    koreans = {}
    for user in korean_queries.get_korean_list():
        team_name = korean_queries.get_team_name_by_user(user)
        if team_name == '':
            team_name = u'회장단'

        if team_name not in koreans:
            koreans[team_name] = []

        score = 0
        attend = TeamAttend.objects.filter(event=event, user=user)
        if attend.exists():
            score = attend[0].score

        score = request.POST.get('score_' + str(user.id), score)
        koreans[team_name].append((user, score))

    for value in koreans.itervalues():
        value = sorted(value, key=lambda x: x[0].profile.korean_name)
    koreans = reversed(sorted(koreans.iteritems()))

    return render(request, 'evaluation/add_team_activity.html', {
        'form': form,
        'koreans': koreans,
    })


@login_required
@group_required('Korean')
def remove_team_activity(request, event_id):
    if not is_team_leader(request.user):
        return redirect(evaluation_status)
    event = get_object_or_404(TeamEvent, id=event_id)
    # TODO: Make restriction by evaluation.

    if event.team == korean_queries.get_team_by_user(request.user):
        TeamAttend.objects.filter(event=event).delete()
        event.delete()

    return redirect(evaluation_status)


# REPORTING PART
@login_required
@group_required('Korean')
def add_personal_report(request):
    month = korean_queries.get_target_month()
    if korean_queries.exist_personal_report(request.user, month):
        return render(request, 'evaluation/exist_report.html', {})

    form = PersonalReportForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        report = form.save(commit=False)
        report.user = request.user
        report.season = get_this_season()
        report.month = month
        report.save()
        return redirect(evaluation_status)

    return render(request, 'evaluation/add_personal_report.html', {
        'form': form,
        'month': month,
    })


@login_required
@group_required('Korean')
def view_personal_report(request, report_id):
    report = get_object_or_404(PersonalReport, id=report_id)
    if report.user != request.user and \
            not request.user.goups.filter(name='Admin').exists():
        return redirect(evaluation_status)

    return render(request, 'evaluation/view_personal_report.html', {
        'report': report,
    })


@login_required
@group_required('Korean')
def remove_personal_report(request, report_id):
    report = get_object_or_404(PersonalReport, id=report_id)
    if report.user == request.user:
        report.delete()

    return redirect(evaluation_status)


# LISTING PART
@login_required
@group_required('Admin')
def korean_list(request):
    users = korean_queries.get_korean_list('birth')
    teams = Team.objects.filter(season=get_this_season())
    groups = BuddyGroup.objects.filter(season=get_this_season())

    infos = []
    for user in users:
        exist = has_matching(user)
        userteam = korean_queries.get_userteam_by_user(user)
        usergroup = korean_queries.get_usergroup_by_user(user)
        infos.append([user, exist, userteam, usergroup])

    return render(request, 'korean/korean_list.html', {
        'infos': infos,
        'teams': teams,
        'groups': groups
    })


@login_required
@group_required('Admin')
def full_list(request):
    season = get_this_season()
    groups = BuddyGroup.objects.filter(season=get_this_season())
    infos = []
    for group in groups:
        usergroups = UserGroup.objects.filter(group=group)
        inner_info = [[x, [[y, ApplicationForeigner.objects.get(user=y,
                                                                season=season)]
                           for y in get_personal_buddies_by_user(x.user)]]
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

    target_users = map(lambda x: get_user(int(x)),
                       request.POST.getlist('checked_ids'))

    try:
        team = request.POST.get('team', None)
        team_leader = request.POST.get('team_leader', None)
        group = request.POST.get('group', None)
        group_leader = request.POST.get('group_leader', None)

        if team or team_leader:
            # Team
            if team is not None:
                team = int(team)
                team = Team.objects.get(id=team) if team != 0 else 0

            for user in target_users:
                if team_leader:
                    korean_queries.make_team_leader(user)
                else:
                    korean_queries.make_team_member(user, team)
        elif group or group_leader:
            # Group
            if group is not None:
                group = BuddyGroup.objects.get(id=int(group))

            for user in target_users:
                if group_leader:
                    korean_queries.make_group_leader(user, group_leader)
                else:
                    korean_queries.make_group_member(user, group)
    except:
        pass

    return redirect(korean_list)
