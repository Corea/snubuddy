# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

from base.queries import get_this_season
from base.decorators import admin_required

from application.models import ApplicationForeigner
from application.forms import ApplicationForeignerForm


@login_required
def index(request):
    return render(request, 'application/index.html', {})


@admin_required
@login_required
def list(request):
    application_list = ApplicationForeigner.objects.filter(
        season=get_this_season())
    return render(request, 'application/list.html', {
        'application_list': application_list
    })


@login_required
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
def register_finish(request):
    return render(request, 'application/register_finish.html', {})
