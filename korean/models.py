# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from base.models import Season


# Team
class Team(models.Model):
    season = models.ForeignKey(Season, null=False)
    name = models.CharField(max_length=64, null=False)

    def __unicode__(self):
        return u'%s - %s' % (self.season, self.name)


class UserTeam(models.Model):
    """Stores team information of Korean buddies"""
    team = models.ForeignKey(Team, null=False)
    user = models.ForeignKey(User, null=False)
    is_leader = models.BooleanField(default=False)

    def __unicode__(self):
        return u' '.join([unicode(self.team.season),
                          u'-', self.user.profile.korean_name,
                          u'-', unicode(self.team),
                          u'Leader' if self.is_leader else u''])


# Group
class BuddyGroup(models.Model):
    season = models.ForeignKey(Season, null=False)
    name = models.CharField(max_length=64, null=False)

    def __unicode__(self):
        return u'%s - %s' % (self.season, self.name)


class UserGroup(models.Model):
    """Stores group information of Korean buddies"""
    NOTHING = 0
    LEADER = 1
    SUBLEADER = 2
    LEADER_CHOICES = (
        (NOTHING, u''),
        (LEADER, u'조장'),
        (SUBLEADER, u'부조장'),
    )

    group = models.ForeignKey(BuddyGroup, null=False)
    user = models.ForeignKey(User, null=False)
    leader_type = models.IntegerField(
        choices=LEADER_CHOICES, default=0, null=False)

    def __unicode__(self):
        return u' '.join([unicode(self.group.season),
                          u'-', self.user.profile.korean_name,
                          u'-', unicode(self.group),
                          dict(self.LEADER_CHOICES)[self.leader_type]])


# Activity
class PersonalEvent(models.Model):
    CAMPUS = 0
    NEAR_CAMPUS = 1
    METROPOLITAN_AREA = 2
    OTHER = 3
    PLACE_CHOICES = (
        (CAMPUS, u'교내'),
        (NEAR_CAMPUS, u'학교 근처'),
        (METROPOLITAN_AREA, u'수도권'),
        (OTHER, u'수도권 외'),
    )

    user = models.ForeignKey(User, null=False)
    season = models.ForeignKey(Season, null=False)
    title = models.CharField(max_length=256, null=False)
    start_date = models.DateField(null=False)
    place = models.CharField(max_length=256, null=False)
    place_type = models.IntegerField(choices=PLACE_CHOICES, null=False)
    photo = models.FileField(
        max_length=1024, upload_to='image/', null=False)

    def __unicode__(self):
        arr = [self.user.profile.korean_name,
               unicode(self.start_date),
               dict(self.PLACE_CHOICES)[self.place_type],
               unicode(self.place),
               unicode(self.title)]

        return u'/'.join(arr)


class GroupEvent(models.Model):
    CAMPUS = 0
    NEAR_CAMPUS = 1
    METROPOLITAN_AREA = 2
    OTHER = 3
    KOREAN = 4
    PLACE_CHOICES = (
        (CAMPUS, u'교내'),
        (NEAR_CAMPUS, u'학교 근처'),
        (METROPOLITAN_AREA, u'수도권'),
        (OTHER, u'수도권 외'),
        (KOREAN, u'한국인 모임'),
    )

    host = models.ForeignKey(User, null=False)
    group = models.ForeignKey(BuddyGroup, null=False)
    title = models.CharField(max_length=256, null=False)
    start_date = models.DateField(null=False)
    place = models.CharField(max_length=256, null=False)
    place_type = models.IntegerField(choices=PLACE_CHOICES, null=False)

    def __unicode__(self):
        arr = [unicode(self.group),
               unicode(self.start_date),
               dict(self.PLACE_CHOICES)[self.place_type],
               unicode(self.place),
               unicode(self.title)]

        return u'/'.join(arr)


class GroupAttend(models.Model):
    event = models.ForeignKey(GroupEvent, null=False)
    user = models.ForeignKey(User, null=False)

    def __unicode__(self):
        return u' '.join([self.user.profile.korean_name,
                          unicode(self.event)])


class TeamEvent(models.Model):
    team = models.ForeignKey(Team, null=False)
    title = models.CharField(max_length=256, null=False)
    start_date = models.DateField(null=False)

    def __unicode__(self):
        arr = [unicode(self.team), unicode(self.start_date), self.title]

        return u'/'.join(arr)


class TeamAttend(models.Model):
    event = models.ForeignKey(TeamEvent, null=False)
    user = models.ForeignKey(User, null=False)
    score = models.IntegerField(null=False)

    def __unicode__(self):
        return u' '.join([self.user.profile.korean_name,
                          unicode(self.event), unicode(self.score)])


class PersonalReport(models.Model):
    user = models.ForeignKey(User, null=False)
    season = models.ForeignKey(Season, null=False)
    month = models.IntegerField(null=False)
    question1 = models.TextField(null=False, blank=True)
    question2 = models.TextField(null=False, blank=True)
    question3 = models.TextField(null=False, blank=True)
    question4 = models.TextField(null=False, blank=True)
    question5 = models.TextField(null=False, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u' '.join([self.user.profile.korean_name,
                          unicode(self.season),
                          unicode(self.month) + u'월'])
