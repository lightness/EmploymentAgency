#coding: utf-8
import django
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import BaseFormView, FormView, ProcessFormView
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from app.models import *
from app.forms import *
from app.forms import UserWithEmailCreationForm
from app.view_mixins import *
from django.core import mail
from django.contrib import auth


RECORDS_PER_PAGE = 5


class AfterLoginRedirectView(RedirectView):
    url_for_admin = reverse_lazy('admin:index')
    url_for_employer = reverse_lazy('EmployerHome')
    url_for_applicant = reverse_lazy('ApplicantHome')
    url_for_new = reverse_lazy('ChooseRole')

    def get_redirect_url(self, *args, **kwargs):
        employers = Employer.objects.filter(profile__user__id=self.request.user.id)
        applicants = Applicant.objects.filter(profile__user__id=self.request.user.id)
        if self.request.user.is_staff:
            return self.url_for_admin
        if len(employers) == 1:
            return self.url_for_employer
        elif len(applicants) == 1:
            return self.url_for_applicant
        return self.url_for_new


class ToMyResponseRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        vacancy_id = kwargs['pk']
        my_response_id = Response.objects.get(vacancy__id=vacancy_id, applicant__profile=self.request.user.profile).id
        return reverse('ShowResponse', args=(my_response_id,))


class AboutView(AlertMixin, TemplateView):
    template_name = "app/other/about.html"


class RegisterSuccessView(TemplateView):
    template_name = "registration/registered.html"


class AccessDeniedView(TemplateView):
    template_name = "app/other/access_denied.html"


class HomeView(TemplateView):
    template_name = "app/other/home.html"


class ChooseRoleView(FormView):
    template_name = "app/other/choose_role.html"
    form_class = ChooseRoleForm
    employer_success_url = reverse_lazy('EmployerHome')
    applicant_success_url = reverse_lazy('ApplicantHome')
    default_success_url = reverse_lazy('About')

    def post(self, request, *args, **kwargs):
        role = request.POST["role"]
        profile = Profile.objects.create(user=request.user)
        if role == "EMP":
            Employer.objects.create(profile=profile)
            return HttpResponseRedirect(self.employer_success_url)
        elif role == "APP":
            Applicant.objects.create(profile=profile)
            return HttpResponseRedirect(self.applicant_success_url)
        return HttpResponseRedirect(self.default_success_url)


class UserCreateView(CreateView):
    model = auth.get_user_model()
    form_class = UserWithEmailCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('Registered')
    email_subject = 'Test message'
    email_body = 'Hello world!'
    email_from = 'registration@empagency.com'

    def form_valid(self, form):
        mail.send_mail(self.email_subject, self.email_body, self.email_from, [form.cleaned_data["email"]])
        return super(UserCreateView, self).form_valid(form)


class ApplicantHomeView(HomePageAlertMixin, DenyIfNotApplicantMixin, TemplateView):
    template_name = "app/other/applicant_home.html"
    cnt_last_vacancies = 3
    cnt_my_last_responses = 3
    cnt_my_last_applications = 3

    def get_context_data(self, **kwargs):
        last_vacancies = Vacancy.objects.order_by('-publish_date')[:self.cnt_last_vacancies]
        applicant = Applicant.objects.get(profile=self.request.user.profile)
        my_last_responses = Response.objects.filter(applicant=applicant).order_by('-response_date')[
                            :self.cnt_my_last_responses]
        my_last_applications = Application.objects.filter(applicant=applicant).order_by('-publish_date')[
                               :self.cnt_my_last_applications]

        context = super(ApplicantHomeView, self).get_context_data()
        context['last_vacancies'] = last_vacancies
        context['my_last_responses'] = my_last_responses
        context['my_last_applications'] = my_last_applications
        context['applicant'] = applicant
        return context


class EmployerHomeView(HomePageAlertMixin, DenyIfNotEmployerMixin, TemplateView):
    template_name = "app/other/employer_home.html"
    cnt_last_applications = 3
    cnt_last_responses_for_my_vacancies = 3
    cnt_my_last_vacancies = 3

    def get_context_data(self, **kwargs):
        last_applications = Application.objects.order_by('-publish_date')[:self.cnt_last_applications]
        employer = Employer.objects.get(profile=self.request.user.profile)
        last_responses_for_my_vacancies = Response.objects.filter(vacancy__employer=employer).order_by(
            '-response_date')[:self.cnt_last_responses_for_my_vacancies]
        my_last_vacancies = Vacancy.objects.filter(employer=employer).order_by('-publish_date')[
                            :self.cnt_my_last_vacancies]

        context = super(EmployerHomeView, self).get_context_data()
        context['last_applications'] = last_applications
        context['last_responses_for_my_vacancies'] = last_responses_for_my_vacancies
        context['my_last_vacancies'] = my_last_vacancies
        context['employer'] = employer
        return context


class VacanciesListView(AlertMixin, SelfnamedMixin, TagSearchMixin, PageHeaderMixin, ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'app/vacancy/list.html'
    paginate_by = RECORDS_PER_PAGE
    form_class = TagForm
    my_name = 'Vacancies'
    page_header = 'Все вакансии'


class MyVacanciesListView(DenyIfNotEmployerMixin, SelfnamedMixin, TagSearchMixin, PageHeaderMixin, ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'app/vacancy/list.html'
    paginate_by = RECORDS_PER_PAGE
    form_class = TagForm
    my_name = 'MyVacancies'
    page_header = 'Мои вакансии'

    def get_queryset(self):
        queryset = super(MyVacanciesListView, self).get_queryset()
        queryset = queryset.filter(employer__profile=self.request.user.profile)
        return queryset


class VacancyCreateView(FormVacancyPageAlertMixin, DenyIfNotEmployerMixin, CreateView):
    model = Vacancy
    form_class = VacancyForm
    context_object_name = 'vacancy'
    template_name = 'app/vacancy/form.html'
    success_url = reverse_lazy('Vacancies')

    def get_form_kwargs(self):
        new_kwargs = super(VacancyCreateView, self).get_form_kwargs()
        new_kwargs['initial']['employer'] = Employer.objects.get(profile=self.request.user.profile)
        return new_kwargs


class VacancyUpdateView(FormVacancyPageAlertMixin, DenyIfEmployerNotOwnerMixin, UpdateView):
    model = Vacancy
    form_class = VacancyForm
    context_object_name = 'vacancy'
    template_name = 'app/vacancy/form.html'
    success_url = reverse_lazy('Vacancies')


class VacancyDeleteView(DenyIfEmployerNotOwnerMixin, DeleteView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'app/vacancy/delete.html'
    success_url = reverse_lazy('Vacancies')


class ResponseCreateView(DenyIfNotApplicantMixin, CreateView):
    model = Response
    form_class = ResponseForm
    context_object_name = 'response'
    template_name = 'app/response/form.html'
    success_url = reverse_lazy('Vacancies')

    def redirect_if_denied(self):
        redirect = super(ResponseCreateView, self).redirect_if_denied()
        if redirect:
            return redirect
        else:
            vacancy = Vacancy.objects.get(pk=self.kwargs['pk'])
            if Response.objects.filter(vacancy=vacancy, applicant__profile=self.request.user.profile).count() > 0:
                my_response_id = Response.objects.get(vacancy=vacancy, applicant__profile=self.request.user.profile).id
                return HttpResponseRedirect(reverse('ShowResponse', args=(my_response_id,)))

    def get_form_kwargs(self):
        new_kwargs = super(ResponseCreateView, self).get_form_kwargs()
        applicant = Applicant.objects.get(profile=self.request.user.profile)
        new_kwargs['initial']['applicant'] = applicant
        new_kwargs['initial']['vacancy'] = Vacancy.objects.get(pk=self.kwargs['pk'])
        new_kwargs['initial']['text'] = applicant.default_response()
        return new_kwargs


class ResponseDetailView(RedirectIfDenyMixin, DetailView):
    model = Response
    context_object_name = 'response'
    template_name = 'app/response/detail.html'

    def redirect_if_denied(self):
        profile = self.request.user.profile
        response = self.get_object()
        if profile.is_employer():
            if response.vacancy.employer.profile != profile:
                return HttpResponseRedirect(reverse('AccessDenied'))
        elif profile.is_applicant():
            if response.applicant.profile != profile:
                return HttpResponseRedirect(reverse('AccessDenied'))


class MyResponsesListView(DenyIfNotApplicantMixin, SelfnamedMixin, TagSearchMixin, PageHeaderMixin, ListView):
    model = Response
    context_object_name = 'responses'
    template_name = 'app/response/list.html'
    paginate_by = RECORDS_PER_PAGE
    form_class = TagForm
    my_name = 'MyResponses'
    page_header = 'Мои отклики'

    def get_queryset(self):
        queryset = super(MyResponsesListView, self).get_queryset()
        queryset = queryset.filter(applicant__profile=self.request.user.profile)
        return queryset


class ResponsesForMyVacanciesListView(DenyIfNotEmployerMixin, SelfnamedMixin, TagSearchMixin, PageHeaderMixin, ListView):
    model = Response
    form_class = TagForm
    context_object_name = 'responses'
    template_name = 'app/response/list.html'
    paginate_by = RECORDS_PER_PAGE
    my_name = 'ResponsesForMyVacancies'
    page_header = 'Отклики на мои вакансии'

    def get_queryset(self):
        queryset = super(ResponsesForMyVacanciesListView, self).get_queryset()
        queryset = queryset.filter(vacancy__employer__profile=self.request.user.profile)
        return queryset


class VacancyDetailView(DetailView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'app/vacancy/detail.html'

    def get_context_data(self, **kwargs):
        context = super(VacancyDetailView, self).get_context_data()
        vacancy = kwargs['object']
        context['responses'] = Response.objects.filter(vacancy=vacancy)
        if self.request.user.is_authenticated():
            if Response.objects.filter(vacancy=vacancy, applicant__profile=self.request.user.profile).count() > 0:
                context['my_response'] = Response.objects.get(vacancy=vacancy,
                                                              applicant__profile=self.request.user.profile)
        return context


class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'app/profile/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data()
        profile = kwargs['object']
        if profile.is_employer():
            context['employer'] = Employer.objects.get(profile=profile)
        elif profile.is_applicant():
            context['applicant'] = Applicant.objects.get(profile=profile)
        return context


class ProfileUpdateView(ProcessFormView):
    template_name = 'app/profile/form.html'

    def get_profile_form(self):
        profile = self.request.user.profile
        return ProfileForm(self.request.POST or None, instance=profile)

    def get_about_me_form(self):
        profile = self.request.user.profile
        if profile.is_applicant():
            applicant = Applicant.objects.get(profile=profile)
            about_me_form = ApplicantForm(self.request.POST or None, self.request.FILES or None, instance=applicant)
        else:
            employer = Employer.objects.get(profile=profile)
            about_me_form = EmployerForm(self.request.POST or None, self.request.FILES or None, instance=employer)
        return about_me_form

    def get_data_context(self):
        context = {
            'profile': self.get_profile_form(),
            'about_me': self.get_about_me_form()
        }
        return context

    def get_forms_valid(self):
        profile_form = self.get_profile_form()
        about_me_form = self.get_about_me_form()

        return profile_form.is_valid() and about_me_form.is_valid()

    def save_forms(self):
        profile_form = self.get_profile_form()
        about_me_form = self.get_about_me_form()
        profile_form.save()
        about_me_form.save()

    def get(self, request, *args, **kwargs):
        self.request = request
        context = self.get_data_context()
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        self.request = request
        if self.get_forms_valid():
            self.save_forms()
            return HttpResponseRedirect(reverse('ShowProfile', args=(request.user.profile.id,)))
        context = self.get_data_context()
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))


class ApplicationCreateView(FormApplicationPageAlertMixin, DenyIfNotApplicantMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    context_object_name = 'application'
    template_name = 'app/application/form.html'
    success_url = reverse_lazy('MyApplications')

    def get_form_kwargs(self):
        new_kwargs = super(ApplicationCreateView, self).get_form_kwargs()
        new_kwargs['initial']['applicant'] = Applicant.objects.get(profile=self.request.user.profile)
        return new_kwargs


class ApplicationUpdateView(FormApplicationPageAlertMixin, DenyIfApplicantNotOwnerMixin, UpdateView):
    model = Application
    form_class = ApplicationForm
    context_object_name = 'application'
    template_name = 'app/application/form.html'
    success_url = reverse_lazy('MyApplications')


class ApplicationListView(SelfnamedMixin, TagSearchMixin, PageHeaderMixin, ListView):
    model = Application
    form_class = TagForm
    context_object_name = 'applications'
    template_name = 'app/application/list.html'
    paginate_by = RECORDS_PER_PAGE
    my_name = 'Applications'
    page_header = 'Все заявления'


class MyApplicationListView(DenyIfNotApplicantMixin, SelfnamedMixin, TagSearchMixin, PageHeaderMixin, ListView):
    model = Application
    form_class = TagForm
    context_object_name = 'applications'
    template_name = 'app/application/list.html'
    paginate_by = RECORDS_PER_PAGE
    my_name = 'MyApplications'
    page_header = 'Мои заявления'

    def get_queryset(self):
        queryset = super(MyApplicationListView, self).get_queryset()
        queryset = queryset.filter(applicant__profile=self.request.user.profile)
        return queryset


class ApplicationDeleteView(DenyIfApplicantNotOwnerMixin, DeleteView):
    model = Application
    context_object_name = 'application'
    template_name = 'app/application/delete.html'
    success_url = reverse_lazy('MyApplications')


class ApplicationDetailView(DetailView):
    model = Application
    context_object_name = 'application'
    template_name = 'app/application/detail.html'