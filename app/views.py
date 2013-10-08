from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
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


class ApplicantHomeView(TemplateView):
    template_name = "applicant_home.html"


class EmployerHomeView(TemplateView):
    template_name = "employer_home.html"


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







class VacanciesListView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'app/vacancy/list.html'
    paginate_by = 20


class VacancyCreateView(CreateView):
    model = Vacancy
    form_class = VacancyForm
    context_object_name = 'vacancy'
    template_name = 'app/vacancy/form.html'
    success_url = reverse_lazy('Vacancies')

    def get(self, request, *args, **kwargs):
        redirect = self.redirect_if_denied()
        if redirect:
            return redirect
        else:
            return super(VacancyCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        redirect = self.redirect_if_denied()
        if redirect:
            return redirect
        else:
            return super(VacancyCreateView, self).post(request, *args, **kwargs)

    def redirect_if_denied(self):
        profile = self.request.user.profile
        if not profile.is_employer():
            return HttpResponseRedirect(reverse('AccessDenied'))

    def get_form_kwargs(self):
        new_kwargs = super(VacancyCreateView, self).get_form_kwargs()
        new_kwargs['initial']['employer'] = Employer.objects.get(profile=self.request.user.profile)
        return new_kwargs


class VacancyUpdateView(UpdateView):
    model = Vacancy
    form_class = VacancyForm
    context_object_name = 'vacancy'
    template_name = 'app/vacancy/form.html'
    success_url = reverse_lazy('Vacancies')

    def get(self, request, *args, **kwargs):
        redirect = self.redirect_if_denied()
        if redirect:
            return redirect
        else:
            return super(VacancyUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        redirect = self.redirect_if_denied()
        if redirect:
            return redirect
        else:
            return super(VacancyUpdateView, self).post(request, *args, **kwargs)

    def redirect_if_denied(self):
        profile = self.request.user.profile
        if not profile.is_employer():
            return HttpResponseRedirect(reverse('AccessDenied'))
        obj = super(VacancyUpdateView, self).get_object()
        if profile.id != obj.employer.profile.id:
            return HttpResponseRedirect(reverse('AccessDenied'))


class VacancyDeleteView(DeleteView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'app/vacancy/delete.html'
    success_url = reverse_lazy('Vacancies')

    def get(self, request, *args, **kwargs):
        redirect = self.redirect_if_denied()
        if redirect:
            return redirect
        else:
            return super(VacancyDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        redirect = self.redirect_if_denied()
        if redirect:
            return redirect
        else:
            return super(VacancyDeleteView, self).post(request, *args, **kwargs)

    def redirect_if_denied(self):
        profile = self.request.user.profile
        if not profile.is_employer():
            return HttpResponseRedirect(reverse('AccessDenied'))
        obj = super(VacancyDeleteView, self).get_object()
        if profile.id != obj.employer.profile.id:
            return HttpResponseRedirect(reverse('AccessDenied'))