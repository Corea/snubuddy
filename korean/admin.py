# -*- coding: utf-8 -*-

from django.contrib import admin
from korean.models import (
    Team, UserTeam, BuddyGroup, UserGroup,
    PersonalEvent, GroupEvent, GroupAttend, TeamEvent, TeamAttend,
    PersonalReport, TeamReport, TeamEvaluation, GroupReport, GroupEvaluation
)


admin.site.register(Team)
admin.site.register(UserTeam)
admin.site.register(BuddyGroup)
admin.site.register(UserGroup)

admin.site.register(PersonalEvent)
admin.site.register(GroupEvent)
admin.site.register(GroupAttend)
admin.site.register(TeamEvent)
admin.site.register(TeamAttend)
admin.site.register(PersonalReport)
admin.site.register(GroupReport)
admin.site.register(GroupEvaluation)
admin.site.register(TeamReport)
admin.site.register(TeamEvaluation)
