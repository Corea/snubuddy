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
from base.forms import RegistrationForm, SettingsForm


def index(request):
    return render(request, 'index.html', {})


def register(request):
    form = RegistrationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        #user = authenticate(username=form.cleaned_data['username'],
        #                    password=form.cleaned_data['password1'])
        #login(request, user)
        return redirect('/account/login/')

    return render(request, 'account/register.html', {
        'form': form
    })


@login_required
def setting(request):
    user = request.user
    form = SettingsForm(request.POST or None,
                        initial={'first_name': user.first_name,
                                 'last_name': user.last_name,
                                 'email': user.email,
                                 'korean_name': user.profile.korean_name,
                                 'gender': user.profile.gender,
                                 'birth': user.profile.birth,
                                 'country': user.profile.country})
    form.user = user

    if request.method == 'POST' and form.is_valid():
        form.save(user)
        return redirect(index)

    return render(request, 'account/setting.html', {
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
