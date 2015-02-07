# -*- coding: utf-8 -*-

import datetime
import re

from django import template
from django.utils.safestring import mark_safe

from matching.models import MatchingConnection


register = template.Library()

class_re = re.compile(r'(?<=class=["\'])(.*)(?=["\'])')


@register.filter
def add_class(value, css_class):
    string = unicode(value)
    match = class_re.search(string)
    if match:
        m = re.search(r'^%s$|^%s\s|\s%s\s|\s%s$' % (css_class, css_class,
                                                    css_class, css_class),
                                                    match.group(1))
        if not m:
            return mark_safe(class_re.sub(match.group(1) + " " + css_class,
                string))
    else:
        return mark_safe(string.replace('>', ' class="%s">' % css_class))
    return value


@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def get_profile(user):
    return UserProfile.objects.get(user=user)


@register.filter
def age(birthday):
    today = datetime.date.today()
    return (today.year - birthday.year) - int((today.month, today.day) <
                                              (birthday.month, birthday.day))


@register.filter
def get_count_matched_buddies(matching):
    return MatchingConnection.objects.filter(korean_matching=matching).count()


@register.filter
def get_level_display(level):
    levels = ['Beginner', 'Intermediate', 'Advanced', 'Fluent']
    return levels[level-1]
