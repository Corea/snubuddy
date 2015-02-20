from django.db import models
from django.contrib.auth.models import User

from base.models import Season, Language


# Buddy Matching
class Matching(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    Both = 'B'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (Both, 'Both'),
    )

    user = models.ForeignKey(User)
    season = models.ForeignKey(Season)
    major = models.CharField(max_length=64, null=False)
    hobby = models.CharField(max_length=128, null=False)
    interest = models.CharField(max_length=128, null=False)
    self_introduction = models.TextField(null=False)
    comment = models.TextField(null=False)

    gender_preference = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True)
    max_buddy_number = models.IntegerField(null=True)

    def __unicode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)


class MatchingLanguage(models.Model):
    matching = models.ForeignKey(Matching)
    language = models.ForeignKey(Language)
    level = models.IntegerField(null=False)

    def __unicode__(self):
        return u'%s %s %s' % (self.matching, self.language, self.level)


class MatchingConnection(models.Model):
    korean_matching = models.ForeignKey(Matching, related_name='korean')
    foreign_matching = models.ForeignKey(Matching, related_name='foreign')

    def __unicode__(self):
        return u'%s - %s' % (self.korean_matching, self.foreign_matching)
