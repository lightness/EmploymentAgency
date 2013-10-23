from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.contrib.auth.views import *
from django.conf import settings
from django.conf.urls.static import static
from app import views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/accounts/login/')),
    url(r'^agency/', include('app.urls')),

    url(r'^accounts/profile/$', views.view_route_after_login, name='RouteAfterLogin'),
    url(r"^accounts/register/success/$", views.RegisterSuccessView.as_view(), name='Registered'),
    url(r'^accounts/register/$', views.view_register, name='Register'),
    url(r'^accounts/login/$',  login, name='Login'),
    url(r'^accounts/logout/$', logout_then_login, { 'next_page': '/agency/home/' }, name='Logout'),

    url(r'^accounts/password/reset/$',  password_reset, {'post_reset_redirect' : '/accounts/password/reset/done/'}),
    url(r'^accounts/password/reset/done/$',  password_reset_done),
    url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'post_reset_redirect' : '/accounts/password/done/'}),
    url(r'^accounts/password/done/$', password_reset_complete),


    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
