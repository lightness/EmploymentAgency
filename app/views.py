from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from app.models import *
from app.forms import UserWithEmailCreationForm


def view_route_after_login(request):
    employers = Employer.objects.filter(user__id=request.user.id)
    applicants = Applicant.objects.filter(user__id=request.user.id)
    if len(employers) == 1:
        return HttpResponseRedirect(reverse('EmployerHome'))
    elif len(applicants) == 1:
        return HttpResponseRedirect(reverse('ApplicantHome'))
    return HttpResponseRedirect(reverse('ChooseRole'))


class AboutView(TemplateView):
    template_name = "about.html"


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
        if role == "EMP":
            Employer.objects.create(user=request.user)
            return HttpResponseRedirect(reverse('EmployerHome'))
        elif role == "APP":
            Applicant.objects.create(user=request.user)
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