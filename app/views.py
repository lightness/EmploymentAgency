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

RECORDS_PER_PAGE = 5

def view_route_after_login(request):
    employers = Employer.objects.filter(profile__user__id=request.user.id)
    applicants = Applicant.objects.filter(profile__user__id=request.user.id)
    if len(employers) == 1:
        return HttpResponseRedirect(reverse('EmployerHome'))
    elif len(applicants) == 1:
        return HttpResponseRedirect(reverse('ApplicantHome'))
    return HttpResponseRedirect(reverse('ChooseRole'))


class AboutView(TemplateView):
    template_name = "about.html"


class AccessDeniedView(TemplateView):
    template_name = "access_denied.html"


class HomeView(TemplateView):
    template_name = "home.html"


def view_choose_role(request):
    template_name = "choose_role.html"

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

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Login'))

    context = {
        'form': form
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))


class RedirectIfDenyMixin(object):
    def get(self, request, *args, **kwargs):
        redirect = self.redirect_if_denied()
        if redirect:
            return redirect
        else:
            return super(RedirectIfDenyMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        redirect = self.redirect_if_denied()
        if redirect:
            return redirect
        else:
            return super(RedirectIfDenyMixin, self).post(request, *args, **kwargs)


class DenyIfNotEmployerMixin(RedirectIfDenyMixin):
    def redirect_if_denied(self):
        profile = self.request.user.profile
        if not profile.is_employer():
            return HttpResponseRedirect(reverse('AccessDenied'))


class DenyIfNotApplicantMixin(RedirectIfDenyMixin):
    def redirect_if_denied(self):
        profile = self.request.user.profile
        if not profile.is_applicant():
            return HttpResponseRedirect(reverse('AccessDenied'))


class DenyIfEmployerNotOwnerMixin(DenyIfNotEmployerMixin):
    def redirect_if_denied(self):
        redirect = super(DenyIfEmployerNotOwnerMixin, self).redirect_if_denied()
        if redirect:
            return redirect
        else:
            obj = super(DenyIfEmployerNotOwnerMixin, self).get_object()
            if self.request.user.profile.id != obj.employer.profile.id:
                return HttpResponseRedirect(reverse('AccessDenied'))


class DenyIfApplicantNotOwnerMixin(DenyIfNotApplicantMixin):
    def redirect_if_denied(self):
        redirect = super(DenyIfApplicantNotOwnerMixin, self).redirect_if_denied()
        if redirect:
            return redirect
        else:
            obj = super(DenyIfApplicantNotOwnerMixin, self).get_object()
            if self.request.user.profile.id != obj.applicant.profile.id:
                return HttpResponseRedirect(reverse('AccessDenied'))


class ApplicantHomeView(DenyIfNotApplicantMixin, TemplateView):
    template_name = "app/applicant_home.html"
    cnt_last_vacancies = 3
    cnt_my_last_responses = 3
    cnt_my_last_CVs = 3

    def get_context_data(self, **kwargs):
        last_vacancies = Vacancy.objects.order_by('-publish_date')[:self.cnt_last_vacancies]
        applicant = Applicant.objects.get(profile=self.request.user.profile)
        my_last_responses = Response.objects.filter(applicant=applicant).order_by('-response_date')[:self.cnt_my_last_responses]
        my_last_CVs = Application.objects.filter(applicant=applicant).order_by('-publish_date')[:self.cnt_my_last_CVs]

        context = super(ApplicantHomeView, self).get_context_data()
        context['last_vacancies'] = last_vacancies
        context['my_last_responses'] = my_last_responses
        context['my_last_CVs'] = my_last_CVs
        context['applicant'] = applicant
        return context


class EmployerHomeView(DenyIfNotEmployerMixin, TemplateView):
    template_name = "app/employer_home.html"
    cnt_last_CVs = 3
    cnt_last_responses_for_my_vacancies = 3
    cnt_my_last_vacancies = 3

    def get_context_data(self, **kwargs):
        last_CVs = Application.objects.order_by('-publish_date')[:self.cnt_last_CVs]
        employer = Employer.objects.get(profile=self.request.user.profile)
        last_responses_for_my_vacancies = Response.objects.filter(vacancy__employer=employer).order_by('-response_date')[:self.cnt_last_responses_for_my_vacancies]
        my_last_vacancies = Vacancy.objects.filter(employer=employer).order_by('-publish_date')[:self.cnt_my_last_vacancies]

        context = super(EmployerHomeView, self).get_context_data()
        context['last_CVs'] = last_CVs
        context['last_responses_for_my_vacancies'] = last_responses_for_my_vacancies
        context['my_last_vacancies'] = my_last_vacancies
        context['employer'] = employer
        return context


class VacanciesListView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'app/vacancy/list.html'
    paginate_by = RECORDS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(VacanciesListView, self).get_context_data()
        context['page_header'] = 'Все вакансии'
        return context


class VacancyCreateView(DenyIfNotEmployerMixin, CreateView):
    model = Vacancy
    form_class = VacancyForm
    context_object_name = 'vacancy'
    template_name = 'app/vacancy/form.html'
    success_url = reverse_lazy('Vacancies')

    def get_form_kwargs(self):
        new_kwargs = super(VacancyCreateView, self).get_form_kwargs()
        new_kwargs['initial']['employer'] = Employer.objects.get(profile=self.request.user.profile)
        return new_kwargs


class VacancyUpdateView(DenyIfEmployerNotOwnerMixin, UpdateView):
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
    template_name = 'app/vacancy/response.html'
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


class ResponseDetailView(DenyIfApplicantNotOwnerMixin, DetailView):
    model = Response
    context_object_name = 'response'
    template_name = 'app/vacancy/detail_response.html'


def view_route_to_my_response(request, **kwargs):
    vacancy_id = kwargs['pk']
    my_response_id = Response.objects.get(vacancy__id=vacancy_id, applicant__profile=request.user.profile).id
    return HttpResponseRedirect(reverse('ShowResponse', args=(my_response_id,)))


class MyResponsesListView(DenyIfNotApplicantMixin, ListView):
    model = Response
    context_object_name = 'responses'
    template_name = 'app/vacancy/my_responses.html'
    paginate_by = RECORDS_PER_PAGE


class MyVacanciesListView(DenyIfNotEmployerMixin, ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'app/vacancy/list.html'
    paginate_by = RECORDS_PER_PAGE

    def get_queryset(self):
        return Vacancy.objects.filter(employer__profile=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super(MyVacanciesListView, self).get_context_data()
        context['page_header'] = 'Мои вакансии'
        return context


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
    template_name = 'app/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data()
        profile = kwargs['object']
        if profile.is_employer():
            context['employer'] = Employer.objects.get(profile=profile)
        elif profile.is_applicant():
            context['applicant'] = Applicant.objects.get(profile=profile)
        return context

def view_update_my_profile(request):
    template_name = 'app/profile.html'

    profile = request.user.profile
    profile_form = ProfileForm(request.POST or None, instance=profile)

    if profile.is_applicant():
        applicant = Applicant.objects.get(profile=profile)
        about_me_form = ApplicantForm(request.POST or None, instance=applicant)
    else:
        employer = Employer.objects.get(profile=profile)
        about_me_form = EmployerForm(request.POST or None, instance=employer)

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
            return HttpResponseRedirect(reverse('UpdateProfile'))

    context = {
        'profile': profile_form,
        'about_me': about_me_form
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))

# ##############################################

class ApplicationCreateView(DenyIfNotApplicantMixin, CreateView):
    model = Application
    form_class = CvForm
    context_object_name = 'cv'
    template_name = 'app/application/form.html'
    success_url = reverse_lazy('MyCVs')

    def get_form_kwargs(self):
        new_kwargs = super(ApplicationCreateView, self).get_form_kwargs()
        new_kwargs['initial']['applicant'] = Applicant.objects.get(profile=self.request.user.profile)
        return new_kwargs


class ApplicationUpdateView(DenyIfApplicantNotOwnerMixin, UpdateView):
    model = Application
    form_class = CvForm
    context_object_name = 'cv'
    template_name = 'app/application/form.html'
    success_url = reverse_lazy('MyCVs')


class ApplicationListView(ListView):
    model = Application
    context_object_name = 'cvs'
    template_name = 'app/application/list.html'
    paginate_by = RECORDS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(ApplicationListView, self).get_context_data()
        context['page_header'] = 'Все резюме'
        return context


class MyApplicationListView(DenyIfNotApplicantMixin, ListView):
    model = Application
    context_object_name = 'cvs'
    template_name = 'app/application/list.html'
    paginate_by = RECORDS_PER_PAGE

    def get_queryset(self):
        return Application.objects.filter(applicant__profile=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super(MyApplicationListView, self).get_context_data()
        context['page_header'] = 'Мои резюме'
        return context


class ApplicationDeleteView(DenyIfApplicantNotOwnerMixin, DeleteView):
    model = Application
    context_object_name = 'cvs'
    template_name = 'app/application/delete.html'
    success_url = reverse_lazy('MyCVs')


class ApplicationDetailView(DetailView):
    model = Application
    context_object_name = 'cv'
    template_name = 'app/application/detail.html'