# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


# Common
class Season(models.Model):
    """Stores season"""
    year = models.IntegerField(null=False)
    semester = models.IntegerField(null=False)
    is_this_season = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u' '.join([u'%s년' % self.year,
                          u'%s학기' % self.semester,
                          u'(이번학기)' if self.is_this_season else u''])


class Country(models.Model):
    name = models.CharField(max_length=64, null=False, unique=True)

    def __unicode__(self):
        return u'%s' % self.name


class Language(models.Model):
    name = models.CharField(max_length=64, null=False, unique=True)

    def __unicode__(self):
        return u'%s' % self.name


# User
class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    user = models.OneToOneField(User, related_name='profile')
    korean_name = models.CharField(max_length=64, blank=True, null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False)
    birth = models.DateField(null=False)
    country = models.ForeignKey(Country, null=False)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
