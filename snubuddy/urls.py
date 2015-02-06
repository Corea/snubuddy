from django.conf.urls import patterns, include, url
from django.contrib import admin

from base import views as base_views
from application import views as application_views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'snubuddy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', base_views.index, name='index'),
    url(r'^account/register/$',
        base_views.register,
        name='account_register'),
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
    url(r'^application/list/$',
        application_views.list,
        name='application_list'),

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
