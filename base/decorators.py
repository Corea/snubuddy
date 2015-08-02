# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect

from base.queries import get_this_season
from base.models import UserSeason
from application.models import ApplicationForeigner


def new_buddy_required(function):
    def wrap(request, *args, **kwargs):
        application = ApplicationForeigner.objects.get(user=request.user)
        if application.returning:
            return HttpResponseRedirect('/')
        else:
            return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def foreigner_required(function):
    def wrap(request, *args, **kwargs):
        user_season = UserSeason.objects.filter(
            user=request.user, season=get_this_season())
        if not user_season.exists():
            return HttpResponseRedirect('/')

        if user_season[0].user_type == UserSeason.FOREIGNER:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def korean_required(function):
    def wrap(request, *args, **kwargs):
        user_season = UserSeason.objects.filter(
            user=request.user, season=get_this_season())
        if not user_season.exists():
            return HttpResponseRedirect('/')

        if user_season[0].user_type in (UserSeason.ADMIN, UserSeason.KOREAN):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def admin_required(function):
    def wrap(request, *args, **kwargs):
        user_season = UserSeason.objects.filter(
            user=request.user, season=get_this_season())
        if not user_season.exists():
            return HttpResponseRedirect('/')

        if user_season[0].user_type == UserSeason.ADMIN:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def guest_required(function):
    def wrap(request, *args, **kwargs):
        if not UserSeason.objects.filter(
                user=request.user, season=get_this_season()).exists():
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def authorize_required(function):
    def wrap(request, *args, **kwargs):
        if UserSeason.objects.filter(
                user=request.user, season=get_this_season()).exists():
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
