# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect


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
