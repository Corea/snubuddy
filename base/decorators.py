# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect

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


def group_required(group_name):
    def group_required_decorator(function):
        def wrap(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/')

        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
    return group_required_decorator


def reverse_group_required(group_name):
    def reverse_group_required_decorator(function):
        def wrap(request, *args, **kwargs):
            if not request.user.groups.filter(name=group_name).exists():
                return function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/')

        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
    return reverse_group_required_decorator
