#coding: utf-8
from django.conf.urls import patterns, url
from auth import views


urlpatterns = patterns('',
    # http://имя_сайта/auth/login
    url(r"^login/$", views.view_login, name='Login'),

    # http://имя_сайта/auth/register
    url(r"^register/$", views.view_register, name='Register'),

    # http://имя_сайта/auth/recovery
    url(r"^recovery/$", views.view_recovery, name='Recovery'),

)

