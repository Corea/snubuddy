# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from base.models import Season


class ApplicationForeigner(models.Model):
    user = models.ForeignKey(User)
    season = models.ForeignKey(Season)
    returning = models.BooleanField(default=False, null=False)
    snu_id = models.CharField(max_length=16, null=False)
    fb_name = models.CharField(max_length=64, null=False)
    fb_email = models.CharField(max_length=64, null=False)

    def __unicode__(self):
        return u'%s %s %s [%s]' % (self.user.first_name,
                                   self.user.last_name,
                                   self.snu_id,
                                   self.returning)
