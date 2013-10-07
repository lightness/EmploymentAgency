from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.contrib.auth.views import login, logout
from app import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/accounts/login/')),
    url(r'^app/', include('app.urls')),

    url(r'^accounts/register/$', views.view_register, name='Register'),
    url(r'^accounts/login/$',  login, name='Login'),
    url(r'^accounts/logout/$', logout, { 'next_page': '/app/home/' }, name='Logout'),

    url(r'^route/after/login/$', views.view_route_after_login, name='RouteAfterLogin'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),


)
