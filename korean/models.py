from django.db import models


# Team
# class Team(models.Model):
#     """Stores team information of Korean buddies"""
#     season = models.ForeignKey(Season, null=False)
#     user = models.ForeignKey(User, null=False)
#     name = models.CharField(max_length=64, null=False)
#     is_leader = models.BooleanField(default=False)
# 
#     def __unicode__(self):
#         return u' '.join([unicode(self.season),
#                           u'-', self.user.first_name,
#                           u'-', unicode(self.team),
#                           u'Leader' if self.is_leader else u''])
# 
# 
# # Group
# class Group(models.Model):
#     season = models.ForeignKey(Season, null=False)
# # Report
# class Question(models.Model):
#     question = models.CharField(max_length=256)
#     created_on = models.DateTimeField(auto_now_add=True)
#     modified_on = models.DateTimeField(auto_now=True)
# 
#     def __unicode__(self):
#         return u'%s' % self.question
# 
# 
# #class Report(models.Model):
# #    season = models.ForeignKey(Season, null=False)
# #    month = models.IntegerField(null=False)
# #    deadline = models.DateTimeField(null=False)
# #    created_on = models.DateTimeField(auto_now_add=True)
# #    modified_on = models.DateTimeField(auto_now=True)
# 
# 
# #class PersonalReport(models.Model):
# #    report = models.ForeignKey(Report, null=False)
# #    user = models.ForeignKey(User, null=False)
# #    foreign_buddy_name = models.CharField(max_length=64)
# #    created_on = models.DateTimeField(auto_now_add=True)
# #    modified_on = models.DateTimeField(auto_now=True)
# 
# 
# class PersonalActivity(models.Model):
#     # personal_report = models.ForeignKey(PersonalReport, null=False)
#     user = models.ForeignKey(User, null=False)
#     particulars = models.CharField(max_length=256)
#     activity_date = models.DateField()
#     remarks = models.CharField(max_length=256)
#     photo = models.FileField(max_length=1024, upload_to='upload/image/', blank=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     modified_on = models.DateTimeField(auto_now=True)
#     
#     def __unicode__(self):
#         return u' '.join([self.user.first_name,
#                           u'-', unicode(self.activity_date),
#                           u'-', self.remarks,
#                           u'-', self.particulars])
# 
# 
# class PersonalEvaluation(models.Model):
#     # personal_report = models.ForeignKey(PersonalReport, null=False)
#     user = models.ForeignKey(User, null=False)
#     question = models.ForeignKey(Question, null=False)
#     answer = models.TextField(null=False)
#     created_on = models.DateTimeField(auto_now_add=True)
#     modified_on = models.DateTimeField(auto_now=True)
