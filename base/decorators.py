# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect


def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='admin').exists():
             return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
