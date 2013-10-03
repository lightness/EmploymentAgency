from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "about.html"


class ApplicantView(TemplateView):
    template_name = "applicant.html"


class EmployerView(TemplateView):
    template_name = "employer.html"
