#coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from app import views


urlpatterns = patterns('',
    # http://имя_сайта/app/about
    url(r"^about/$", views.AboutView.as_view(), name='About'),

    # http://имя_сайта/app/access/denied/
    url(r"^access/denied/$", views.AccessDeniedView.as_view(), name='AccessDenied'),

    # http://имя_сайта/app/role/choose/
    url(r"^role/choose/$", login_required(views.view_choose_role), name='ChooseRole'),

    # http://имя_сайта/app/home
    url(r"^home/$", views.HomeView.as_view(), name='Home'),

    # http://имя_сайта/app/profile/my/update/
    url(r"^profile/my/update/$", login_required(views.view_update_my_profile), name='UpdateProfile'),

    # http://имя_сайта/app/profile/id/
    url(r"^profile/(?P<pk>\d+)/$", login_required(views.ProfileDetailView.as_view()), name='ShowProfile'),

    # http://имя_сайта/app/home/applicant
    url(r"^home/applicant/$", login_required(views.ApplicantHomeView.as_view()), name='ApplicantHome'),

    # http://имя_сайта/app/home/employer
    url(r"^home/employer/$", login_required(views.EmployerHomeView.as_view()), name='EmployerHome'),

    # http://имя_сайта/app/vacancy/id/response/my/
    url(r"^vacancy/(?P<pk>\d+)/response/my/$", login_required(views.view_route_to_my_response), name='GetMyResponseByVacancy'),

    ####################################################################################################################

    # http://имя_сайта/app/vacancies/
    # http://имя_сайта/app/vacancies/pageN
    url(r"^vacancies/$", views.VacanciesListView.as_view(), name='Vacancies'),
    url(r"^vacancies/page(?P<page>\d+)/$", views.VacanciesListView.as_view(), name='Vacancies'),

    # http://имя_сайта/app/vacancy/create/
    url(r"^vacancy/create/$", login_required(views.VacancyCreateView.as_view()), name='CreateVacancy'),

    # http://имя_сайта/app/vacancy/id/update/
    url(r"^vacancy/(?P<pk>\d+)/update/$", login_required(views.VacancyUpdateView.as_view()), name='UpdateVacancy'),

    # http://имя_сайта/app/vacancy/id/delete/
    url(r"^vacancy/(?P<pk>\d+)/delete/$", login_required(views.VacancyDeleteView.as_view()), name='DeleteVacancy'),

    # http://имя_сайта/app/vacancy/id/
    url(r"^vacancy/(?P<pk>\d+)/$", views.VacancyDetailView.as_view(), name='ShowVacancy'),

    ####################################################################################################################

    # http://имя_сайта/app/vacancy/id/response/create/
    url(r"^vacancy/(?P<pk>\d+)/response/create/$", login_required(views.ResponseCreateView.as_view()), name='CreateResponse'),

    # http://имя_сайта/app/vacancy/response/id/
    url(r"^vacancy/response/(?P<pk>\d+)/$", login_required(views.ResponseDetailView.as_view()), name='ShowResponse'),

    # http://имя_сайта/app/vacancy/responses/my/
    url(r"^vacancy/responses/my/$", login_required(views.MyResponsesListView.as_view()), name='MyResponses'),

    # http://имя_сайта/app/vacancies/my/
    url(r"^vacancies/my/$", login_required(views.MyVacanciesListView.as_view()), name='MyVacancies'),


    # http://имя_сайта/app/CVs/
    url(r"^CVs/$", views.CvListView.as_view(), name='CVs'),

    # http://имя_сайта/app/CVs/my/
    url(r"^CVs/my/$", login_required(views.MyCvListView.as_view()), name='MyCVs'),

    # http://имя_сайта/app/CV/create/
    url(r"^CV/create/$", login_required(views.CvCreateView.as_view()), name='CreateCV'),

    # http://имя_сайта/app/CV/id/update
    url(r"^CV/(?P<pk>\d+)/update/$", login_required(views.CvUpdateView.as_view()), name='UpdateCV'),

    # http://имя_сайта/app/CV/id/
    url(r"^CV/(?P<pk>\d+)/$", views.CvDetailView.as_view(), name='ShowCV'),

    # http://имя_сайта/app/CV/id/delete
    url(r"^CV/(?P<pk>\d+)/delete/$", login_required(views.CvDeleteView.as_view()), name='DeleteCV'),

)

