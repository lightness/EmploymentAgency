from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=30)

    class Meta:
        abstract = True


class Applicant(Profile):
    full_name = models.CharField(max_length=100)


class Employer(Profile):
    title = models.CharField(max_length=100)



