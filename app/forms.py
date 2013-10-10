from django.contrib.auth.forms import UserCreationForm
from django import forms
from app.models import *


class UserWithEmailCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=254)

    def save(self, commit=True):
        user = super(UserWithEmailCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ('publish_date',)
        widgets = {
            'employer': forms.HiddenInput(),
            'profession': forms.TextInput(),
            'position': forms.TextInput(),
            'salary_currency': forms.Select(),
            'salary_min': forms.NumberInput(),
            'salary_max': forms.NumberInput(),
            'age_min': forms.NumberInput(),
            'age_max': forms.NumberInput(),
            'details': forms.Textarea()
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        exclude = ()
        widgets = {
            'applicant': forms.HiddenInput(),
            'vacancy': forms.HiddenInput(),
            'text': forms.Textarea()
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ()
        widgets = {
            'user': forms.HiddenInput(),
            'phone1': forms.TextInput(),
            'phone2': forms.TextInput(),
            'email': forms.TextInput(),
            'skype': forms.TextInput(),
            'icq': forms.TextInput()
        }


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        exclude = ()
        widgets = {
            'profile': forms.HiddenInput(),
            'full_name': forms.TextInput(),
            'birth_date': forms.DateInput()
        }


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        exclude = ()
        widgets = {
            'profile': forms.HiddenInput(),
            'title': forms.TextInput()
        }


class CvForm(forms.ModelForm):
    class Meta:
        model = CV
        exclude = ('publish_date',)
        widgets = {
            'applicant': forms.HiddenInput(),
            'profession': forms.TextInput(),
            'salary_min': forms.NumberInput(),
            'salary_currency': forms.Select(),
            'experience': forms.NumberInput(),
            'details': forms.Textarea()
        }