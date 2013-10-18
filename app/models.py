#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from EmploymentAgency.settings import *


def content_file_name(instance, filename):
    return '/'.join([MEDIA_ROOT, instance.profile.user.username, filename])


CURRENCY = (
    ('BLR', 'Бел. руб.'),
    ('USD', '$'),
    ('EUR', '₠'),
)


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone1 = models.CharField(max_length=30, null=True, blank=True, verbose_name="Телефон №1")
    phone2 = models.CharField(max_length=30, null=True, blank=True, verbose_name="Телефон №2")
    email = models.EmailField(max_length=50, null=True, blank=True, verbose_name="Email")
    skype = models.CharField(max_length=50, null=True, blank=True, verbose_name="Skype")
    icq = models.IntegerField(max_length=9, null=True, blank=True, verbose_name="ICQ")

    def is_applicant(self):
        return Applicant.objects.filter(profile=self).count() > 0

    def is_employer(self):
        return Employer.objects.filter(profile=self).count() > 0

    def __unicode__(self):
        return self.user.username


class Applicant(models.Model):
    profile = models.ForeignKey(Profile)
    full_name = models.CharField(max_length=100, verbose_name="Фамилия Имя Отчество")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    photo = models.ImageField(null=True, blank=True, upload_to=content_file_name, verbose_name="Фото")

    def age(self):
        if self.birth_date is None:
            return None
        return int((date.today() - self.birth_date).days / 365.25)

    def default_response(self):
        hello = u"Здавствуйте. "
        name = u"Меня зовут %s. " % self.full_name
        age = u"Мне %s лет. " % self.age()
        response = u"Я хотел(а) бы с вами сотрудничать. "
        contacts = u"\nСвязаться со мной можно по: "
        phone1 = u"\n > тел. %s." % self.profile.phone1
        phone2 = u"\n > тел. %s." % self.profile.phone2
        email = u"\n > Email: %s. " % self.profile.email
        skype = u"\n > Skype: %s. " % self.profile.skype
        icq = u"\n > ICQ: %s." % self.profile.icq

        text = hello
        if self.full_name:
            text += name
        if self.age() > 0:
            text += age
        text += response + contacts
        if self.profile.phone1:
            text += phone1
        if self.profile.phone2:
            text += phone2
        if self.profile.email:
            text += email
        if self.profile.skype:
            text += skype
        if self.profile.icq:
            text += icq

        return text

    def __unicode__(self):
        return self.profile.user.username


class Employer(models.Model):
    profile = models.ForeignKey(Profile)
    title = models.CharField(max_length=100, verbose_name="Наименование организации")
    logo = models.ImageField(upload_to=content_file_name, verbose_name="Лого")

    def __unicode__(self):
        return self.profile.user.username


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
    publish_date = models.DateTimeField(auto_now=True)

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

    def __unicode__(self):
        organization = u"Предприятию %s " %self.employer.title
        position = u"на должность %s " % self.position
        profession = u"требуется %s. " % self.profession
        salary = u"Заработная плата: "
        salary_min = u"от %s " % self.salary_min
        salary_max = u"до %s " % self.salary_max
        salary_currency = u"%s. " %self.salary_currency
        age = u"Возраст:"
        age_min = u" от %s" % self.age_min
        age_max = u" до %s" % self.age_max
        age_postfix = u" лет. "
        details = u"Дополнительная информация: %s. " % self.details

        text = organization
        if self.position:
            text +=position
        text += profession
        if self.salary_min or self.salary_max:
            text += salary
            if self.salary_min:
                text += salary_min
            if self.salary_max:
                text += salary_max
            text += salary_currency
        if self.age_min or self.age_max:
            text += age
            if self.age_min:
                text += age_min
            if self.age_max:
                text += age_max
            text += age_postfix
        if self.details:
            text += details

        return text


class Response(models.Model):
    applicant = models.ForeignKey(Applicant)
    vacancy = models.ForeignKey(Vacancy)
    text = models.TextField(verbose_name='Текст отклика')
    response_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text

    class Meta:
        unique_together = ("applicant", "vacancy")


class Application(models.Model):
    applicant = models.ForeignKey(Applicant)
    profession = models.CharField(max_length=100)
    salary_min = models.PositiveIntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=10, choices=CURRENCY, blank=True, null=True)
    experience = models.PositiveSmallIntegerField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    publish_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        name = u"Меня зовут %s. " % self.applicant.full_name
        age = u"Мне %s лет. " % self.applicant.age()
        profession = u"Ищу работу по специальности: %s. " % self.profession
        experience = u"Имею опыт работы по специальности: %s лет. " % self.experience
        salary = u"Требования к зарплате: от %s %s. " % (self.salary_min, self.salary_currency)
        details = u"Дополнительная информация: %s. " % self.details

        text = u""
        if self.applicant.full_name:
            text += name
        if self.applicant.age() > 0:
            text += age
        text += profession
        if self.experience:
            text += experience
        if self.salary_min:
            text += salary
        if self.details:
            text += details

        return text


