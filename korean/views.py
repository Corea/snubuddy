# -*- coding: utf-8 -*-

from itertools import groupby
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

from base.templatetags.filters import (
    is_team_leader, is_group_leader, is_group_subleader
)

from application.models import ApplicationForeigner
from korean.models import (
    Team, UserTeam, BuddyGroup, UserGroup,
    PersonalEvent, GroupEvent, GroupAttend, TeamEvent, TeamAttend,
    PersonalReport, TeamReport, TeamEvaluation, GroupReport, GroupEvaluation
)
from base.decorators import group_required

from base.queries import get_this_season, get_user
from matching.queries import get_personal_buddies_by_user, has_matching
from korean.forms import (
    PersonalEventForm, GroupEventForm, TeamEventForm, PersonalReportForm
)

from korean.queries import *


@login_required
@group_required('Korean')
def evaluation_status(request):
    # Events
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
    attended_events = sorted(
        attended_events,
        key=lambda (x, y): y.start_date if x != 'Team' else y.event.start_date)

    personal_type = map(lambda x: x.place_type, personal_events)
    group_type = map(lambda x: x.place_type, group_attended_events)
    personal_scores = [personal_type.count(i) for i in range(4)]
    group_scores = [group_type.count(i) for i in range(5)]
    team_score = sum(map(lambda x: x.score, team_attends))

    # Reports
    personal_report = PersonalReport.objects.filter(
        user=request.user, season=get_this_season())
    reports = map(lambda x: ('Personal', x), personal_report)
    team_events = []
    group_events = []

    if is_team_leader(request.user):
        team = get_team_by_user(request.user)
        team_events = TeamEvent.objects.filter(
            team=team).order_by('start_date')
        team_reports = TeamReport.objects.filter(
            team=team, season=get_this_season())
        reports += map(lambda x: ('Team', x), team_reports)

    if is_group_leader(request.user):
        group = get_buddygroup_by_user(request.user)
        group_events = GroupEvent.objects.filter(
            group=group).order_by('start_date')
        group_reports = GroupReport.objects.filter(
            group=group, season=get_this_season())
        reports += map(lambda x: ('Group', x), group_reports)

    reports = sorted(reports, key=lambda (x, y): (y.month, x))

    return render(request, 'evaluation/status.html', {
        'personal_scores': personal_scores,
        'group_scores': group_scores,
        'team_score': team_score,
        'attended_events': attended_events,
        'personal_events': personal_events,
        'team_events': team_events,
        'group_events': group_events,
        'reports': reports,
    })


@login_required
@group_required('Korean')
def add_personal_activity(request):
    form = PersonalEventForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)

        if exist_personal_report(request.user, event.start_date.month):
            return render(request, 'error.html', {
                'error': u'%s월 평가서를 이미 작성하셨습니다.' % event.start_date.month
            })

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

    if event.user == request.user:
        if exist_personal_report(request.user, event.start_date.month):
            return render(request, 'error.html', {
                'error': u'%s월 평가서를 이미 작성하셨습니다.' % event.start_date.month
            })

        event.delete()

    return redirect(evaluation_status)


@login_required
@group_required('Korean')
def add_group_activity(request):
    if not is_group_leader(request.user):
        return redirect(evaluation_status)
    group = get_buddygroup_by_user(request.user)
    members = map(lambda x: [x, False],
                  sorted(get_member_by_buddygroup(group),
                         key=lambda x: x.profile.korean_name))
    checked_ids = map(int, request.POST.getlist('checked_ids'))

    for member in members:
        if member[0].id in checked_ids:
            member[1] = True

    form = GroupEventForm(group, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)
        if exist_group_report(request.user, event.start_date.month):
            return render(request, 'error.html', {
                'error': u'%s월 평가서를 이미 작성하셨습니다.' % event.start_date.month
            })
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
    if event.group != get_buddygroup_by_user(request.user):
        return redirect(evaluation_status)

    disabled = False
    if exist_group_report(request.user, event.start_date.month):
        disabled = True

    group = get_buddygroup_by_user(request.user)
    members = map(lambda x: [x, False],
                  sorted(get_member_by_buddygroup(group),
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
        if disabled:
            return render(request, 'error.html', {
                'error': u'%s월 평가서를 이미 작성하셨습니다.' % event.start_date.month
            })

        GroupAttend.objects.filter(event=event).delete()
        event = form.save()

        for (user, check) in members:
            if check:
                attend = GroupAttend.objects.create(event=event, user=user)
                attend.save()

        return redirect(evaluation_status)

    return render(request, 'evaluation/modify_group_activity.html', {
        'form': form,
        'members': members,
        'disabled': disabled
    })


@login_required
@group_required('Korean')
def remove_group_activity(request, event_id):
    if not is_group_leader(request.user):
        return redirect(evaluation_status)
    event = get_object_or_404(GroupEvent, id=event_id)

    if event.group == get_buddygroup_by_user(request.user):
        if exist_group_report(request.user, event.start_date.month):
            return render(request, 'error.html', {
                'error': u'%s월 평가서를 이미 작성하셨습니다.' % event.start_date.month
            })
        GroupAttend.objects.filter(event=event).delete()
        event.delete()

    return redirect(evaluation_status)


@login_required
@group_required('Korean')
def add_team_activity(request):
    if not is_team_leader(request.user):
        return redirect(evaluation_status)
    form = TeamEventForm(request.POST or None)
    team = get_team_by_user(request.user)

    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)
        if exist_team_report(team, event.start_date.month):
            return render(request, 'error.html', {
                'error': u'%s월 평가서를 이미 작성하셨습니다.' % event.start_date.month
            })

        event.team = team
        event.save()

        for user in get_korean_list():
            score = float(request.POST.get('score_' + str(user.id), 0))
            if score < 1e-8:
                continue

            attend = TeamAttend.objects.create(
                event=event, user=user, score=score)
            attend.save()

        return redirect(evaluation_status)

    koreans = {}
    for user in get_korean_list():
        team_name = get_team_name_by_user(user)
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
    if event.team != get_team_by_user(request.user):
        return redirect(evaluation_status)

    disabled = False
    if exist_team_report(event.team, event.start_date.month):
        disabled = True

    form = TeamEventForm(request.POST or None, instance=event)
    if request.method == 'POST' and form.is_valid():
        if disabled:
            return render(request, 'error.html', {
                'error': u'%s월 평가서를 이미 작성하셨습니다.' % event.start_date.month
            })
        TeamAttend.objects.filter(event=event).delete()
        event = form.save()

        for user in get_korean_list():
            score = float(request.POST.get('score_' + str(user.id), 0))
            if score < 1e-8:
                continue

            attend = TeamAttend.objects.create(
                event=event, user=user, score=score)
            attend.save()

        return redirect(evaluation_status)

    koreans = {}
    for user in get_korean_list():
        team_name = get_team_name_by_user(user)
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

    return render(request, 'evaluation/modify_team_activity.html', {
        'form': form,
        'koreans': koreans,
        'disabled': disabled,
    })


@login_required
@group_required('Korean')
def remove_team_activity(request, event_id):
    if not is_team_leader(request.user):
        return redirect(evaluation_status)
    event = get_object_or_404(TeamEvent, id=event_id)

    if event.team == get_team_by_user(request.user):
        if exist_team_report(event.team, event.start_date.month):
            return render(request, 'error.html', {
                'error': u'%s월 평가서를 이미 작성하셨습니다.' % event.start_date.month
            })
        TeamAttend.objects.filter(event=event).delete()
        event.delete()

    return redirect(evaluation_status)


# REPORTING PART
@login_required
@group_required('Korean')
def add_personal_report(request):
    month = get_target_month()
    if exist_personal_report(request.user, month):
        return render(request, 'error.html', {
            'error': u'이미 작성하셨습니다.'
        })

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
            not request.user.groups.filter(name='Admin').exists():
        return redirect(evaluation_status)

    return render(request, 'evaluation/view_personal_report.html', {
        'report': report,
    })


@login_required
@group_required('Korean')
def add_group_report(request):
    if not is_group_leader(request.user) and \
            not is_group_subleader(request.user):
        return redirect(evaluation_status)

    month = get_target_month()
    group = get_buddygroup_by_user(request.user)
    if exist_group_report(request.user, month):
        return render(request, 'error.html', {
            'error': u'이미 작성하셨습니다.'
        })

    members = []
    valid = True
    for user in get_member_by_buddygroup(group):
        score1 = request.POST.get('score1_' + str(user.id), '')
        score2 = request.POST.get('score2_' + str(user.id), '')
        reason = request.POST.get('reason_' + str(user.id), u'')
        error = u''

        if request.method == 'POST' and \
                score1 not in '012345' or score2 not in '012345':
            error = u'점수를 선택해주세요.'
            valid = False
        members.append((user, score1, score2, reason, error))

    if request.method == 'POST' and valid:
        report = GroupReport.objects.create(
            user=request.user,
            group=group,
            season=get_this_season(),
            month=month)

        for user, score1, score2, reason, _ in members:
            evaluation = GroupEvaluation.objects.create(
                report=report, user=user,
                score1=int(score1), score2=int(score2), reason=reason)
            evaluation.save()

        return redirect(evaluation_status)

    return render(request, 'evaluation/add_group_report.html', {
        'month': month,
        'members': members,
    })


@login_required
@group_required('Korean')
def view_group_report(request, id):
    report = get_object_or_404(GroupReport, id=id)
    if report.user != request.user and \
            not request.user.groups.filter(name='Admin').exists():
        return redirect(evaluation_status)

    evaluations = GroupEvaluation.objects.filter(
        report=report).order_by('user__profile__korean_name')

    return render(request, 'evaluation/view_group_report.html', {
        'report': report,
        'evaluations': evaluations,
    })


@login_required
@group_required('Korean')
def add_team_report(request):
    if not is_team_leader(request.user):
        return redirect(evaluation_status)
    month = get_target_month()
    team = get_team_by_user(request.user)
    if exist_team_report(team, month):
        return render(request, 'error.html', {
            'error': u'이미 작성하셨습니다.'
        })

    members = []
    valid = True
    for user in get_member_by_team(team):
        grade = request.POST.get('grade_' + str(user.id), '')
        reason = request.POST.get('reason_' + str(user.id), u'')
        error = u''
        if request.method == 'POST' and grade not in ('0', '1', '2', '3'):
            error = u'선택해주세요.'
            valid = False
        members.append((user, grade, reason, error))

    if request.method == 'POST' and valid:
        report = TeamReport.objects.create(
            user=request.user,
            team=team,
            season=get_this_season(),
            month=month)

        for user, grade, reason, _ in members:
            evaluation = TeamEvaluation.objects.create(
                report=report, user=user,
                grade=int(grade), reason=reason)
            evaluation.save()

        return redirect(evaluation_status)

    return render(request, 'evaluation/add_team_report.html', {
        'month': month,
        'members': members,
    })


@login_required
@group_required('Admin')
def view_team_report(request, id):
    report = get_object_or_404(TeamReport, id=id)
    evaluations = TeamEvaluation.objects.filter(
        report=report).order_by('user__profile__korean_name')

    return render(request, 'evaluation/view_team_report.html', {
        'report': report,
        'evaluations': evaluations,
    })


# LISTING PART
@login_required
@group_required('Admin')
def korean_list(request):
    users = get_korean_list('birth')
    teams = Team.objects.filter(season=get_this_season())
    groups = BuddyGroup.objects.filter(season=get_this_season())

    infos = []
    for user in users:
        exist = has_matching(user)
        userteam = get_userteam_by_user(user)
        usergroup = get_usergroup_by_user(user)
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
                    make_team_leader(user)
                else:
                    make_team_member(user, team)
        elif group or group_leader:
            # Group
            if group is not None:
                group = BuddyGroup.objects.get(id=int(group))

            for user in target_users:
                if group_leader:
                    make_group_leader(user, group_leader)
                else:
                    make_group_member(user, group)
    except:
        pass

    return redirect(korean_list)


@login_required
@group_required('Admin')
def secret(request):
    picture = (request.GET.get('picture', None) == 'true')
        
    personal_events = PersonalEvent.objects.filter(
        season=get_this_season()
    ).order_by('start_date', 'user__profile__korean_name')
    group_events = GroupEvent.objects.filter(
        group__season=get_this_season()
    ).order_by('start_date', 'group__name')
    team_events = TeamEvent.objects.filter(
        team__season=get_this_season()
    ).order_by('start_date', 'team__name')

    personal_reports = PersonalReport.objects.filter(
        season=get_this_season()).order_by('month', 'user__profile__korean_name')
    team_reports = TeamReport.objects.filter(
        season=get_this_season()).order_by('month')
    group_reports = GroupReport.objects.filter(
        season=get_this_season()).order_by('month', 'group__name')

    return render(request, 'evaluation/secret.html', {
        'picture': picture,
        'personal_events': personal_events,
        'group_events': group_events,
        'team_events': team_events,
        'personal_reports': personal_reports,
        'group_reports': group_reports,
        'team_reports': team_reports,
    })
