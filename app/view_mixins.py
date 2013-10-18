#coding: utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from app.classes import Alert
from app.models import *


class AlertMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AlertMixin, self).get_context_data(**kwargs)
        context['alerts'] = self.collect_alerts()
        return context

    def collect_alerts(self):
        pass


class ApplicantHomePageAlertMixin(AlertMixin):
    def collect_alerts(self):
        alerts = ()
        alerts += self.append_if_need_fill_phones()
        # TODO: Add more alerts
        return alerts

    def append_if_need_fill_phones(self):
        if not self.request.user.is_authenticated():
            return ()
        profile = self.request.user.profile
        alerts = ()
        if profile.is_applicant():
            if not profile.phone1 and not profile.phone2:
                alert = Alert('Заполните, пожалуйста, контактный телефон.', alert_class='alert-warning',
                              button_text='Заполнить', button_class='btn-warning', button_redirect_url='UpdateProfile')
                alerts += (alert,)
        return alerts


class CreateApplicationPageAlertMixin(AlertMixin):
    def collect_alerts(self):
        alerts = ()
        alerts += self.append_if_need_fill_info()
        alerts += self.append_if_need_fill_contact_info()
        return alerts

    def append_if_need_fill_info(self):
        if not self.request.user.is_authenticated():
            return ()
        profile = self.request.user.profile
        applicant = Applicant.objects.get(profile=profile)
        alerts = ()
        if not applicant.full_name:
            alert = Alert('Заполните, пожалуйста, ФИО.', alert_class='alert-danger',
                          button_text='Заполнить', button_class='btn-danger', button_redirect_url='UpdateProfile')
            alerts += (alert,)
        if not applicant.birth_date:
            alert = Alert('Заполните, пожалуйста, дату рождения.', alert_class='alert-danger',
                          button_text='Заполнить', button_class='btn-danger', button_redirect_url='UpdateProfile')
            alerts += (alert,)
        if not applicant.photo:
            alert = Alert('Загрузите свое фото!', alert_class='alert-warning',
                          button_text='Загрузить', button_class='btn-warning', button_redirect_url='UpdateProfile')
            alerts += (alert,)
        return alerts

    def append_if_need_fill_contact_info(self):
        if not self.request.user.is_authenticated():
            return ()
        profile = self.request.user.profile
        alerts = ()
        if not profile.phone1 and not profile.phone2 and not profile.email and not profile.icq and not profile.skype:
            alert = Alert('Заполните контактную информацию. Иначе работодатели не смогут с вами связаться.',
                          alert_class='alert-danger',button_text='Заполнить', button_class='btn-danger',
                          button_redirect_url='UpdateProfile')
            alerts += (alert,)
        return alerts



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
