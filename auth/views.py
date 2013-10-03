from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
from django.template import RequestContext

def view_login(request):
    template_name = "auth/login.html"
    context = {

    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def view_register(request):
    template_name = "auth/register.html"
    context = {

    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))


