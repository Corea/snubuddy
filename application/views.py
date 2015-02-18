# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

from base.queries import get_this_season
from base.decorators import group_required

from application.models import ApplicationForeigner
from application.forms import ApplicationForeignerForm

from matching.models import Matching


@login_required
def index(request):
    if request.user.groups.filter(name='Admin').exists():
        return redirect(list)
    if request.user.groups.filter(name='Guest').exists():
        return redirect(register)
    return redirect('/')


@login_required
@group_required('Admin')
def list(request):
    application_infos = []
    application_list = ApplicationForeigner.objects.filter(
        season=get_this_season()).order_by('id')
    for application in application_list:
        exist = Matching.objects.filter(
            user=application.user,
            season=get_this_season()).exists()
        application_infos.append([application, exist])
 
    return render(request, 'application/list.html', {
        'application_infos': application_infos
    })


@login_required
@group_required('Admin')
def accept(request, application_id):
    application = ApplicationForeigner.objects.get(id=application_id)
    user = application.user
    user.groups.add(Group.objects.get(name='Foreigner'))
    user.groups.remove(Group.objects.get(name='Guest'))
    return redirect(list)


@login_required
@group_required('Guest')
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
@group_required('Guest')
def register_finish(request):
    return render(request, 'application/register_finish.html', {})
