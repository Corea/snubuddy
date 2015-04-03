# -8_ coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from application import views as application_views
from base import views as base_views
from matching import views as matching_views
from korean import views as korean_views


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^upload/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}),

    url(r'^$', base_views.index, name='index'),
    url(r'^account/register/$',
        base_views.register,
        name='account_register'),
    url(r'^account/setting/$',
        base_views.setting,
        name='account_setting'),
    url(r'^account/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'account/login.html'}),
    url(r'^account/logout/$', 'django.contrib.auth.views.logout',
        kwargs={'next_page': '/'}),

    url(r'^application/$',
        application_views.index,
        name='application_index'),
    url(r'^application/register/$',
        application_views.register,
        name='application_register'),
    url(r'^application/register_finish/$',
        application_views.register_finish,
        name='application_register_finish'),
    url(r'^application/list/$',
        application_views.list,
        name='application_list'),
    url(r'^application/accept/(?P<application_id>\d+)/$',
        application_views.accept,
        name='application_accept'),

    url(r'^matching/$',
        matching_views.list,
        name='matching_index'),
    url(r'^matching/register/$',
        matching_views.register,
        name='matching_register'),
    url(r'^matching/view/(?P<id>\d+)/$',
        matching_views.view,
        name='matching_view'),
    url(r'^matching/register/(?P<id>\d+)/$',
        matching_views.register_foreigner,
        name='matching_register_foreigner'),
    url(r'^matching/register_full/$',
        matching_views.register_full,
        name='matching_register_full'),
    url(r'^matching/delete/(?P<id>\d+)/$',
        matching_views.delete,
        name='matching_delete'),
    url(r'^matching/delete/bye/(?P<id>\d+)/$',
        matching_views.delete_bye,
        name='matching_delete_bye'),

    url(r'^korean/korean_list/$',
        korean_views.korean_list,
        name='korean_korean_list'),
    url(r'^korean/full_list/$',
        korean_views.full_list,
        name='korean_full_list'),
    url(r'^korean/make_member/$',
        korean_views.make_member,
        name='korean_make_member'),

    url(r'^evaluation/$',
        korean_views.evaluation_status,
        name='evaluation_status'),

    url(r'^evaluation/personal_activity/$',
        korean_views.add_personal_activity,
        name='evaluation_add_personal_activity'),
    url(r'^evaluation/group_activity/$',
        korean_views.add_group_activity,
        name='evaluation_add_group_activity'),
    url(r'^evaluation/team_activity/$',
        korean_views.add_team_activity,
        name='evaluation_add_team_activity'),

    url(r'^evaluation/group_activity/(\d+)/$',
        korean_views.modify_group_activity,
        name='evaluation_modify_group_activity'),
    url(r'^evaluation/team_activity/(\d+)/$',
        korean_views.modify_team_activity,
        name='evaluation_modify_team_activity'),

    url(r'^evaluation/personal_activity/remove/(\d+)/$',
        korean_views.remove_personal_activity,
        name='evaluation_remove_personal_activity'),
    url(r'^evaluation/group_activity/remove/(\d+)/$',
        korean_views.remove_group_activity,
        name='evaluation_remove_group_activity'),
    url(r'^evaluation/team_activity/remove/(\d+)/$',
        korean_views.remove_team_activity,
        name='evaluation_remove_team_activity'),

    url(r'^evaluation/personal_report/$',
        korean_views.add_personal_report,
        name='evaluation_add_personal_report'),
    url(r'^evaluation/personal_report/(\d+)/$',
        korean_views.view_personal_report,
        name='evaluation_view_personal_report'),

    url(r'^evaluation/group_report/$',
        korean_views.add_group_report,
        name='evaluation_add_group_report'),
    url(r'^evaluation/group_report/(\d+)/$',
        korean_views.view_group_report,
        name='evaluation_view_group_report'),

    url(r'^evaluation/team_report/$',
        korean_views.add_team_report,
        name='evaluation_add_team_report'),
    url(r'^evaluation/team_report/(\d+)/$',
        korean_views.view_team_report,
        name='evaluation_view_team_report'),

    url(r'^evaluation/SECRET/$',
        korean_views.secret,
        name='evaluation_secret'),
)
