from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from app.models import *
from app.forms import *
from app.forms import UserWithEmailCreationForm


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
        super(DenyIfEmployerNotOwnerMixin, self).redirect_if_denied()
        obj = super(DenyIfEmployerNotOwnerMixin, self).get_object()
        if self.request.user.profile.id != obj.employer.profile.id:
            return HttpResponseRedirect(reverse('AccessDenied'))


class DenyIfApplicantNotOwnerMixin(DenyIfNotApplicantMixin):
    def redirect_if_denied(self):
        super(DenyIfApplicantNotOwnerMixin, self).redirect_if_denied()
        obj = super(DenyIfApplicantNotOwnerMixin, self).get_object()
        if self.request.user.profile.id != obj.applicant.profile.id:
            return HttpResponseRedirect(reverse('AccessDenied'))


class ApplicantHomeView(DenyIfNotApplicantMixin, TemplateView):
    template_name = "applicant_home.html"
    cnt_last_vacancies = 3
    cnt_my_last_responses = 3

    def get_context_data(self, **kwargs):
        last_vacancies = Vacancy.objects.order_by('-publish_date')[:self.cnt_last_vacancies]
        my_last_responses = Response.objects.filter(applicant__profile=self.request.user.profile).order_by('-response_date')[:self.cnt_my_last_responses]

        context = super(ApplicantHomeView, self).get_context_data()
        context['last_vacancies'] = last_vacancies
        context['my_last_responses'] = my_last_responses
        return context


class EmployerHomeView(DenyIfNotEmployerMixin, TemplateView):
    template_name = "employer_home.html"


class VacancyDetailView(DetailView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'app/vacancy/detail.html'


class VacanciesListView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'app/vacancy/list.html'
    paginate_by = 20


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
    form_class = VacancyResponseForm
    context_object_name = 'response'
    template_name = 'app/vacancy/response.html'
    success_url = reverse_lazy('Vacancies')

    def get_form_kwargs(self):
        new_kwargs = super(ResponseCreateView, self).get_form_kwargs()
        new_kwargs['initial']['applicant'] = Applicant.objects.get(profile=self.request.user.profile)
        new_kwargs['initial']['vacancy'] = Vacancy.objects.get(pk=self.kwargs['pk'])
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
    paginate_by = 20


class MyVacanciesListView(DenyIfNotEmployerMixin, ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'app/vacancy/my.html'
    paginate_by = 20

    def get_queryset(self):
        return Vacancy.objects.filter(employer__profile=self.request.user.profile)
