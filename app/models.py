#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone1 = models.CharField(max_length=30, null=True, blank=True)
    phone2 = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    skype = models.CharField(max_length=50, null=True, blank=True)
    icq = models.IntegerField(max_length=9, null=True, blank=True)

    def is_applicant(self):
        return Applicant.objects.filter(profile=self).count() > 0

    def is_employer(self):
        return Employer.objects.filter(profile=self).count() > 0

class Applicant(models.Model):
    profile = models.ForeignKey(Profile)
    full_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)


class Employer(models.Model):
    profile = models.ForeignKey(Profile)
    title = models.CharField(max_length=100)


CURRENCY = (
    ('BLR', 'Бел. руб.'),
    ('USD', '$'),
    ('EUR', '₠'),
)


class Vacancy(models.Model):
    employer = models.ForeignKey(Employer)
    profession = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)
    salary_currency = models.CharField(max_length=10, choices=CURRENCY, blank=True, null=True)
    salary_min = models.PositiveIntegerField(blank=True, null=True)
    salary_max = models.PositiveIntegerField(blank=True, null=True)
    age_min = models.PositiveSmallIntegerField(blank=True, null=True)
    age_max = models.PositiveSmallIntegerField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    date_publish = models.DateTimeField(auto_now=True) # Need test

    def responses_count(self):
        return 0

    def clean(self):
        if self.age_min and self.age_max:
            if self.age_min > self.age_max:
                raise ValidationError('Минимальный возраст не может быть больше максимального')
        if self.salary_min and self.salary_max:
            if self.salary_min > self.salary_max:
                raise ValidationError('Минимальная З/П не может быть больше максимальной')
        if self.salary_min or self.salary_max:
            if not self.salary_currency:
                raise ValidationError('Укажите денежную единицу для З/П')


class CV(models.Model):
    applicant = models.ForeignKey(Applicant)
    profession = models.CharField(max_length=100)
    salary_min = models.PositiveIntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=10, choices=CURRENCY, blank=True, null=True)
    experience = models.PositiveSmallIntegerField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)


