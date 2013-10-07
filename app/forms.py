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
        fields = (
            'employer', 'profession', 'position', 'salary_currency', 'salary_min', 'salary_max', 'age_min', 'age_max',
            'details',
        )
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






