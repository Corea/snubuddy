# -*- coding: utf-8 -*-

from django.contrib import admin
from korean.models import (
    Team, UserTeam
)


admin.site.register(Team)
admin.site.register(UserTeam)
