#coding: utf-8
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from app.models import *
from app.forms import *
from app.forms import UserWithEmailCreationForm
from app.view_mixins import *
from django.core import mail


RECORDS_PER_PAGE = 5


def view_route_after_login(request):
    employers = Employer.objects.filter(profile__user__id=request.user.id)
    applicants = Applicant.objects.filter(profile__user__id=request.user.id)
    if len(employers) == 1:
        return HttpResponseRedirect(reverse('EmployerHome'))
    elif len(applicants) == 1:
        return HttpResponseRedirect(reverse('ApplicantHome'))
    return HttpResponseRedirect(reverse('ChooseRole'))


class AboutView(AlertMixin, TemplateView):
    template_name = "app/other/about.html"


class RegisterSuccessView(TemplateView):
    template_name = "registration/registered.html"


class AccessDeniedView(TemplateView):
    template_name = "app/other/access_denied.html"


class HomeView(TemplateView):
    template_name = "app/other/home.html"


def view_choose_role(request):
    template_name = "app/other/choose_role.html"

    if request.method == "POST":
        role = request.POST["role"]
        profile = Profile.objects.create(user=request.user)
        if role == "EMP":
            Employer.objects.create(profile=profile)
            return HttpResponseRedirect(reverse('EmployerHome'))
        elif role == "APP":
            Applicant.objects.create(profile=profile)
            return HttpResponseRedirect(reverse('ApplicantHome'))
        return HttpResponseRedirect(reverse('About'))

    context = {}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def view_register(request):
    template_name = "registration/register.html"
    form = UserWithEmailCreationForm(request.POST or None)
    email_subject = 'Test message'
    email_body = 'Hello world!'
    email_from = 'registration@empagency.com'

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            mail.send_mail(email_subject, email_body, email_from, [form.cleaned_data["email"]])
            return HttpResponseRedirect(reverse('Registered'))

    context = {
        'form': form
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))


class ApplicantHomeView(ApplicantHomePageAlertMixin, DenyIfNotApplicantMixin, TemplateView):
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


class EmployerHomeView(DenyIfNotEmployerMixin, TemplateView):
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


def view_route_to_my_response(request, **kwargs):
    vacancy_id = kwargs['pk']
    my_response_id = Response.objects.get(vacancy__id=vacancy_id, applicant__profile=request.user.profile).id
    return HttpResponseRedirect(reverse('ShowResponse', args=(my_response_id,)))


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


def view_update_my_profile(request):
    template_name = 'app/profile/form.html'

    profile = request.user.profile
    profile_form = ProfileForm(request.POST or None, instance=profile)

    if profile.is_applicant():
        applicant = Applicant.objects.get(profile=profile)
        about_me_form = ApplicantForm(request.POST or None, request.FILES or None, instance=applicant)
    else:
        employer = Employer.objects.get(profile=profile)
        about_me_form = EmployerForm(request.POST or None, request.FILES or None, instance=employer)

    if request.method == 'POST':
        valid = True

        if profile_form.is_valid():
            profile_form.save()
        else:
            valid = False

        if about_me_form.is_valid():
            about_me_form.save()
        else:
            valid = False

        if valid:
            return HttpResponseRedirect(reverse('ShowProfile', args=(profile.id,)))

    context = {
        'profile': profile_form,
        'about_me': about_me_form
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))

# ##############################################

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