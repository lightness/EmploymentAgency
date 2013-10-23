from django.contrib.auth.forms import UserCreationForm
from django import forms
from app.models import *
from app.widgets import *



class TagForm(forms.Form):
    tag = forms.CharField(required=False)


class UserWithEmailCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=254)

    def save(self, commit=True):
        user = super(UserWithEmailCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ('publish_date',)
        widgets = {
            'employer': forms.HiddenInput(),
            'profession': BootstrapTextInput(),
            'position': BootstrapTextInput(),
            'salary_currency': BootstrapSelect(),
            'salary_min': BootstrapNumberInput(),
            'salary_max': BootstrapNumberInput(),
            'age_min': BootstrapNumberInput(),
            'age_max': BootstrapNumberInput(),
            'details': BootstrapTextarea()
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        exclude = ()
        widgets = {
            'applicant': forms.HiddenInput(),
            'vacancy': forms.HiddenInput(),
            'text': BootstrapTextarea()
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ()
        widgets = {
            'user': forms.HiddenInput(),
            'phone1': BootstrapTextInput(),
            'phone2': BootstrapTextInput(),
            'email': BootstrapTextInput(),
            'skype': BootstrapTextInput(),
            'icq': BootstrapTextInput()
        }


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        exclude = ()
        widgets = {
            'profile': forms.HiddenInput(),
            'full_name': BootstrapTextInput(),
            'birth_date': BootstrapDateInput()
        }


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        exclude = ()
        widgets = {
            'profile': forms.HiddenInput(),
            'title': BootstrapTextInput(),
            'logo': forms.ClearableFileInput()
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ('publish_date',)
        widgets = {
            'applicant': forms.HiddenInput(),
            'profession': BootstrapTextInput(),
            'salary_min': BootstrapNumberInput(),
            'salary_currency': BootstrapSelect(),
            'experience': BootstrapNumberInput(),
            'details': BootstrapTextarea()
        }