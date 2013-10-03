from django.conf.urls import patterns, include, url
from  django.views.generic.base import RedirectView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/auth/login/')),

    url(r'^app/', include('app.urls')),
    url(r'^auth/', include('auth.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
