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
    is_language_exchange = models.BooleanField(default=False, null=False)
    is_confirm = models.BooleanField(default=False, null=False)

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
    is_lunch = models.BooleanField(default=False, null=False)
    is_confirm = models.BooleanField(default=False, null=False)

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
    score = models.FloatField(null=False)

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


class TeamReport(models.Model):
    user = models.ForeignKey(User, null=False)
    team = models.ForeignKey(Team, null=False)
    season = models.ForeignKey(Season, null=False)
    month = models.IntegerField(null=False)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u' '.join([unicode(self.team),
                          unicode(self.season),
                          unicode(self.month) + u'월'])


class TeamEvaluation(models.Model):
    A = 0
    B = 1
    C = 2
    D = 3
    GRADE_CHOICES = (
        (A, u'A'),
        (B, u'B'),
        (C, u'C'),
        (D, u'D'),
    )

    report = models.ForeignKey(TeamReport, null=False)
    user = models.ForeignKey(User, null=False)
    grade = models.IntegerField(choices=GRADE_CHOICES, null=False)
    reason = models.CharField(max_length=512, null=False, blank=True)

    def __unicode__(self):
        return u' '.join([self.user.profile.korean_name,
                          unicode(self.report.season),
                          unicode(self.report.month) + u'월',
                          unicode(dict(self.GRADE_CHOICES)[self.grade])])


class GroupReport(models.Model):
    user = models.ForeignKey(User, null=False)
    group = models.ForeignKey(BuddyGroup, null=False)
    season = models.ForeignKey(Season, null=False)
    month = models.IntegerField(null=False)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u' '.join([self.user.profile.korean_name,
                          unicode(self.group),
                          unicode(self.season),
                          unicode(self.month) + u'월'])


class GroupEvaluation(models.Model):
    report = models.ForeignKey(GroupReport, null=False)
    user = models.ForeignKey(User, null=False)
    score1 = models.IntegerField(null=False)
    score2 = models.IntegerField(null=False)
    reason = models.CharField(max_length=512, null=False, blank=True)

    def __unicode__(self):
        return u' '.join([unicode(self.report),
                          self.user.profile.korean_name])


class MonthlyScore(models.Model):
    user = models.ForeignKey(User, null=False)
    season = models.ForeignKey(Season, null=False)
    month = models.IntegerField(null=False)
    count_personal_0 = models.IntegerField(default=0, null=False)
    count_personal_1 = models.IntegerField(default=0, null=False)
    count_personal_2 = models.IntegerField(default=0, null=False)
    count_personal_3 = models.IntegerField(default=0, null=False)
    count_group_0 = models.IntegerField(default=0, null=False)
    count_group_1 = models.IntegerField(default=0, null=False)
    count_group_2 = models.IntegerField(default=0, null=False)
    count_group_3 = models.IntegerField(default=0, null=False)
    count_group_4 = models.IntegerField(default=0, null=False)
    score_personal = models.FloatField(default=0, null=False)
    score_group = models.FloatField(default=0, null=False)
    score_team = models.FloatField(default=0, null=False)
    score_full = models.FloatField(default=0, null=False)

    def __unicode__(self):
        return u' '.join([self.user.profile.korean_name,
                          unicode(self.month) + u'월',
                          unicode(self.score_personal),
                          unicode(self.score_group),
                          unicode(self.score_team)])
