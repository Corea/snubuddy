from django.contrib import admin

from base.models import (
    Season, Country, Language, UserProfile, UserSeason
)


admin.site.register(Season)
admin.site.register(Country)
admin.site.register(Language)
admin.site.register(UserProfile)
admin.site.register(UserSeason)
