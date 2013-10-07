#coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from app import views


urlpatterns = patterns('',
    # http://имя_сайта/app/about
    url(r"^about/$", login_required(views.AboutView.as_view()), name='About'),

    # http://имя_сайта/app/home
    url(r"^home/$", views.HomeView.as_view(), name='Home'),

    # http://имя_сайта/app/home/applicant
    url(r"^home/applicant/$", views.ApplicantHomeView.as_view(), name='ApplicantHome'),

    # http://имя_сайта/app/home/employer
    url(r"^home/employer/$", views.EmployerHomeView.as_view(), name='EmployerHome'),

    # http://имя_сайта/app/role/choose/
    url(r"^role/choose/$", views.view_choose_role, name='ChooseRole'),



    # http://имя_сайта/app/vacancies/
    url(r"^vacancies/$", views.view_vacancies, name='Vacancies'),

    # http://имя_сайта/app/vacancies/my/
    url(r"^vacancies/my/$", views.view_my_vacancies, name='MyVacancies'),

    # http://имя_сайта/app/vacancies/
    url(r"^vacancy/create/$", views.view_create_vacancy, name='CreateVacancy'),

    # http://имя_сайта/app/vacancy/id/update
    url(r"^vacancy/(?P<id>\d+)/update/$", views.view_update_vacancy, name='UpdateVacancy'),

    # http://имя_сайта/app/vacancy/id/delete
    url(r"^vacancy/(?P<id>\d+)/delete/$", views.view_delete_vacancy, name='DeleteVacancy'),

    # http://имя_сайта/app/vacancy/id/response
    url(r"^vacancy/(?P<id>\d+)/response/$", views.view_response_for_vacancy, name='ResponseForVacancy'),

    # http://имя_сайта/app/vacancy/id/response/delete
    url(r"^vacancy/(?P<id>\d+)/response/delete/$", views.view_delete_response_for_vacancy, name='DeleteResponseForVacancy'),



    # http://имя_сайта/app/CVs/
    url(r"^CVs/$", views.view_CVs, name='CVs'),

    # http://имя_сайта/app/CVs/my/
    url(r"^CVs/$", views.view_my_CVs, name='MyCVs'),

    # http://имя_сайта/app/CV/create/
    url(r"^CV/create/$", views.view_create_CV, name='CreateCV'),

    # http://имя_сайта/app/CV/id/update
    url(r"^CV/(?P<id>\d+)/update/$", views.view_update_CV, name='UpdateCV'),

    # http://имя_сайта/app/CV/id/delete
    url(r"^CV/(?P<id>\d+)/delete/$", views.view_delete_CV, name='DeleteCV'),

    # http://имя_сайта/app/CV/id/response
    url(r"^CV/(?P<id>\d+)/response/$", views.view_response_for_CV, name='ResponseForCV'),

    # http://имя_сайта/app/CV/id/response/delete
    url(r"^CV/(?P<id>\d+)/response/delete/$", views.view_delete_response_for_CV, name='DeleteResponseForCV'),
)

