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
    #url(r'^accounts/register/$', views.view_register, name='Register'),
    url(r'^accounts/register/$', views.UserCreateView.as_view(), name='Register'),
    url(r'^accounts/login/$',  login, name='Login'),
    url(r'^accounts/logout/$', logout_then_login, name='Logout'),

    url(r'^accounts/password/reset/$',  password_reset, {'from_email' : 'registration@empagency.com'}, name='password_reset'),
    url(r'^accounts/password/reset/done/$',  password_reset_done, name='password_reset_done'),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^accounts/password/done/$', password_reset_complete, name='password_reset_complete'),

    url(r'^accounts/password/change/$', password_change, name='password_change'),
    url(r'^accounts/password/change/done/$', password_change_done, name='password_change_done'),


    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
