from django.contrib import admin

from matching.models import Matching, MatchingLanguage, MatchingConnection


admin.site.register(Matching)
admin.site.register(MatchingLanguage)
admin.site.register(MatchingConnection)
