from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserWithEmailCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=254)

    def save(self, commit=True):
        user = super(UserWithEmailCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user





