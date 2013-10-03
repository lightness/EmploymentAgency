#coding: utf-8
from django.conf.urls import patterns, url
from app import views


urlpatterns = patterns('',
    # http://имя_сайта/app/about
    url(r"^about/$", views.AboutView.as_view(), name='About'),

    # http://имя_сайта/app/applicant
    url(r"^applicant/$", views.ApplicantView.as_view(), name='Applicant'),

    # http://имя_сайта/app/employer
    url(r"^employer/$", views.EmployerView.as_view(), name='Employer'),
)

