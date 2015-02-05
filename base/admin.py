from django.contrib import admin

from base.models import (
    Season, Country, Language, UserProfile
)

admin.site.register(Season)
admin.site.register(Country)
admin.site.register(Language)
admin.site.register(UserProfile)
