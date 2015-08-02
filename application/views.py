# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

from base.models import UserSeason
from base.queries import get_this_season
from base.decorators import guest_required, admin_required

from application.models import ApplicationForeigner
from application.forms import ApplicationForeignerForm

from matching.models import Matching


@login_required
def index(request):
    user_season = UserSeason.objects.filter(user=request.user)
    if not user_season.exists():
        return redirect(register)
    return redirect(list)


@login_required
@admin_required
def list(request):
    season = get_this_season()

    application_infos = []
    application_list = ApplicationForeigner.objects.filter(
        season=season).order_by('id')
    for application in application_list:
        matching = Matching.objects.filter(
            user=application.user,
            season=season)
        if matching.exists():
            matching = matching[0]
        application_infos.append([application, matching])

    return render(request, 'application/list.html', {
        'application_infos': application_infos
    })


@login_required
@admin_required
def accept(request, application_id):
    application = ApplicationForeigner.objects.get(id=application_id)
    UserSeason.objects.create(
        user=application.user,
        season=application.season,
        user_type=UserSeason.FOREIGNER).save()
    return redirect(list)


@login_required
@guest_required
def register(request):
    form = ApplicationForeignerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ApplicationForeigner.objects.filter(
            user=request.user,
            season=get_this_season()).delete()
        application = form.save(commit=False)
        application.user = request.user
        application.season = get_this_season()
        application.save()
        return redirect(register_finish)

    application_exist = ApplicationForeigner.objects.filter(
        user=request.user,
        season=get_this_season()).count() > 0

    return render(request, 'application/register.html', {
        'form': form,
        'exists': application_exist
    })


@login_required
@guest_required
def register_finish(request):
    return render(request, 'application/register_finish.html', {})
