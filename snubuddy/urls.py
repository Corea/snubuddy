from django.conf.urls import patterns, include, url
from django.contrib import admin

from application import views as application_views
from base import views as base_views
from matching import views as matching_views
from korean import views as korean_views


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

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

    url(r'^korean/$',
        korean_views.index,
        name='korean_index'),
    url(r'^korean/korean_list/$',
        korean_views.korean_list,
        name='korean_korean_list'),
    url(r'^korean/full_list/$',
        korean_views.full_list,
        name='korean_full_list'),
    url(r'^korean/make_member/$',
        korean_views.make_member,
        name='korean_make_member'),
)
