# -*- coding: utf-8 -*-

from django.contrib import admin
from korean.models import (
    Team, UserTeam, BuddyGroup, UserGroup
)


admin.site.register(Team)
admin.site.register(UserTeam)
admin.site.register(BuddyGroup)
admin.site.register(UserGroup)
