#coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from app import views
from django.core.urlresolvers import reverse, reverse_lazy


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
    url(r"^vacancies/tag/(?P<tag>\w+)/$", views.VacanciesListView.as_view(), name='Vacancies'),
    url(r"^vacancies/page(?P<page>\d+)/$", views.VacanciesListView.as_view(), name='Vacancies'),
    url(r"^vacancies/tag/(?P<tag>\w+)/page(?P<page>\d+)/$", views.VacanciesListView.as_view(), name='Vacancies'),

    # http://имя_сайта/app/vacancies/my/
    url(r"^vacancies/my/$", login_required(views.MyVacanciesListView.as_view()), name='MyVacancies'),
    url(r"^vacancies/my/tag/(?P<tag>\w+)/$", login_required(views.MyVacanciesListView.as_view()), name='MyVacancies'),
    url(r"^vacancies/my/page(?P<page>\d+)/$", login_required(views.MyVacanciesListView.as_view()), name='MyVacancies'),
    url(r"^vacancies/my/tag/(?P<tag>\w+)/page(?P<page>\d+)/$", login_required(views.MyVacanciesListView.as_view()), name='MyVacancies'),


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

    # http://имя_сайта/app/response/id/
    url(r"^response/(?P<pk>\d+)/$", login_required(views.ResponseDetailView.as_view()), name='ShowResponse'),

    # http://имя_сайта/app/vacancy/responses/my/
    url(r"^responses/my/$", login_required(views.MyResponsesListView.as_view()), name='MyResponses'),
    url(r"^responses/my/page(?P<page>\d+)/$", login_required(views.MyResponsesListView.as_view()), name='MyResponses'),
    url(r"^responses/my/tag/(?P<tag>\w+)/$", login_required(views.MyResponsesListView.as_view()), name='MyResponses'),
    url(r"^responses/my/tag/(?P<tag>\w+)/page(?P<page>\d+)/$", login_required(views.MyResponsesListView.as_view()), name='MyResponses'),


    # http://имя_сайта/app/vacancies/my/responses/
    url(r"^vacancies/my/responses/$", login_required(views.ResponsesForMyVacanciesListView.as_view()), name='ResponsesForMyVacancies'),
    url(r"^vacancies/my/responses/page(?P<page>\d+)/$", login_required(views.ResponsesForMyVacanciesListView.as_view()), name='ResponsesForMyVacancies'),
    url(r"^vacancies/my/responses/tag/(?P<tag>\w+)/$", login_required(views.ResponsesForMyVacanciesListView.as_view()), name='ResponsesForMyVacancies'),
    url(r"^vacancies/my/responses/tag/(?P<tag>\w+)/page(?P<page>\d+)/$", login_required(views.ResponsesForMyVacanciesListView.as_view()), name='ResponsesForMyVacancies'),


    # http://имя_сайта/app/applications/
    url(r"^applications/$", views.ApplicationListView.as_view(), name='Applications'),
    url(r"^applications/page(?P<page>\d+)/$", views.ApplicationListView.as_view(), name='Applications'),
    url(r"^applications/tag/(?P<tag>\w+)/$", views.ApplicationListView.as_view(), name='Applications'),
    url(r"^applications/tag/(?P<tag>\w+)/page(?P<page>\d+)/$", views.ApplicationListView.as_view(), name='Applications'),


    # http://имя_сайта/app/applications/my/
    url(r"^applications/my/$", login_required(views.MyApplicationListView.as_view()), name='MyApplications'),
    url(r"^applications/my/page(?P<page>\d+)/$", login_required(views.MyApplicationListView.as_view()), name='MyApplications'),
    url(r"^applications/my/tag/(?P<tag>\w+)/$", login_required(views.MyApplicationListView.as_view()), name='MyApplications'),
    url(r"^applications/my/tag/(?P<tag>\w+)/page(?P<page>\d+)/$", login_required(views.MyApplicationListView.as_view()), name='MyApplications'),


    # http://имя_сайта/app/application/create/
    url(r"^application/create/$", login_required(views.ApplicationCreateView.as_view()), name='CreateApplication'),

    # http://имя_сайта/app/application/id/update
    url(r"^application/(?P<pk>\d+)/update/$", login_required(views.ApplicationUpdateView.as_view()), name='UpdateApplication'),

    # http://имя_сайта/app/application/id/
    url(r"^application/(?P<pk>\d+)/$", views.ApplicationDetailView.as_view(), name='ShowApplication'),

    # http://имя_сайта/app/application/id/delete
    url(r"^application/(?P<pk>\d+)/delete/$", login_required(views.ApplicationDeleteView.as_view()), name='DeleteApplication'),

)

