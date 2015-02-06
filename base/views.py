# -*- coding: utf-8 -*-

import os
import mimetypes

from StringIO import StringIO

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseForbidden

from base import queries
from base.forms import RegistrationForm


def index(request):
    return render(request, 'index.html', {})


def register(request):
    form = RegistrationForm(data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
        login(request, user)
        return redirect(index)

    return render(request, 'account/register.html', {
        'form': form
    })


@login_required
def user_setting(request):
    user = request.user
    form = SettingsForm(data=request.POST or None,
                        initial={'name': user.first_name})

    if request.method == 'POST' and form.is_valid():
        form.save(user)
        return redirect(index)

    return render(request, 'setting.html', {
        'form': form
    })


@login_required
def personal_list(request):
    activities = queries.get_personal_activities(request.user)
    return render(request, 'personal/list.html', {
        'activities': activities
    })


@login_required
def personal_get_photo(request, personal_id):
    activity = queries.get_personal_activity(personal_id)
    if activity.user != request.user:
        return HttpResponseForbidden()
    image = StringIO(file(activity.photo.path, 'rb').read())

    mimetype = mimetypes.guess_type(os.path.basename(activity.photo.name))[0]
    return HttpResponse(image.read(), mimetype)


@login_required
def personal_add(request):
    if request.method == 'POST':
        form = PersonalActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            return redirect(personal_list)
    else:
        form = PersonalActivityForm()

    return render(request, 'personal/add.html', {
        'form': form
    })


@login_required
def personal_delete(request, personal_id):
    activity = queries.get_personal_activity(personal_id)
    if activity.user != request.user:
        return HttpResponseForbidden()
    activity.delete()
    return redirect(personal_list)
