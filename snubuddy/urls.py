from django.conf.urls import patterns, include, url
from django.contrib import admin

from application import views as application_views
from base import views as base_views
from matching import views as matching_views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'snubuddy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

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

    url(r'^matching/$',
        matching_views.list,
        name='matching_index'),
    url(r'^matching/register/$',
        matching_views.register,
        name='matching_register'),
    url(r'^matching/view/(?P<matching_id>\d+)/$',
        matching_views.view,
        name='matching_view'),
    url(r'^matching/register/(?P<matching_id>\d+)/$',
        matching_views.register_foreigner,
        name='matching_register_foreigner'),
    url(r'^matching/register_full/$',
        matching_views.register_full,
        name='matching_register_full'),
    url(r'^matching/delete/(?P<matching_id>\d+)/$',
        matching_views.delete,
        name='matching_delete'),
    url(r'^matching/delete/bye/(?P<matching_id>\d+)/$',
        matching_views.delete_bye,
        name='matching_delete_bye'),

    # url(r'^setting/$', base_views.user_setting, name='setting'),

    # url(r'^personal/$', base_views.personal_list, name='personal_list'),
    # url(r'^personal/get_photo/(\d+)/$', base_views.personal_get_photo, name='personal_get_photo'),
    # url(r'^personal/add/$', base_views.personal_add, name='personal_add'),


    # url(r'^accounts/register/$', register, {
    #     'backend': 'registration.backends.default.DefaultBackend',
    #     'form_class': base_forms.UserRegForm
    # }, name='registration_register'),
    # url(r'^accounts/', include('registration.backends.default.urls')),
)
