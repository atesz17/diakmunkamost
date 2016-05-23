from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.db import models

from helpers.models import TimeStampedModel

class Job(TimeStampedModel):

    '''
    Parsing (es architekturalis) problemak miatt egyelore csak:
        1. Pesti munkakat jelenitek meg a honlapon (nem lehet mezore keresni)
        2. Munkaido is csak text (nem lehet mezore keresni)

    Kesobbi prioritas lesz majd ezen mezok rendes megvalositasa
    '''

    UNDEFINED_SALARY_TEXT = 'Megállapodás szerint'

    PREDEFINED_JOB_TYPES = {
        "fizikai": "Könnyű Fizikai",
        "irodai": "Irodai",
        "telefonos": "Telefonos",
        "hostess": "Hostess",
        "muszaki": "Műszaki",
        "informatikai": "Informatikai",
        "aruhazi/vendeglatos": "Áruházi/Vendéglátós",
        "egyeb": "Egyéb"
    }

    title = models.TextField(verbose_name='Munka megnevezése')
    job_type = models.ForeignKey(
        'JobType',
        on_delete=models.CASCADE,
        verbose_name='Munka típusa'
    )
    job_provider = models.ForeignKey(
        'JobProvider',
        on_delete=models.CASCADE,
        verbose_name='Diákmunka Szövetkezet'
    )
    task = models.TextField(verbose_name='Feladat leírása')
    place_of_work = models.TextField(verbose_name='Munkavégzés helye')
    min_salary = models.IntegerField(
        db_index=True, verbose_name='Minumum órabér'
    )
    max_salary = models.IntegerField(verbose_name='Maximum órabér')
    working_hours = models.TextField(verbose_name='Munkaidő')
    requirements = models.TextField(verbose_name='Feltételek')
    url = models.TextField(
        validators=[URLValidator(schemes=['http', 'https'])],
        unique=True,
        verbose_name='Munka URL címe'
    )
    other_info = models.TextField(blank=True, verbose_name='Egyéb információ')

    def get_absolute_url(self):
        return reverse('jobs:specific_job', args=(self.id,))

    def validate_min_max_salary(self):
        '''
        https://docs.djangoproject.com/en/1.9/_modules/django/db/models/base/#Model.full_clean

        Nem dobunk ValidationError-t, ha valamelyik None, mert azt ugy is meg
        ellenorizni fogja kulon a field required constraint. Csak returnolunk
        '''
        if self.min_salary is None or self.max_salary is None:
            return
        if self.min_salary > self.max_salary:
            msg = "min_salary({0}) cannot be greater than max_salary({1})"
            raise ValidationError(
                msg.format(self.min_salary, self.max_salary)
            )

    def clean(self):
        self.validate_min_max_salary()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Diákmunka"
        verbose_name_plural = "Diákmunkák"


class JobType(models.Model):

    name = models.TextField(
        unique=True,
        verbose_name="Munka típusa"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Munkatípus"
        verbose_name_plural = "Munkatípusok"


class JobProvider(models.Model):

    PROVIDER_FULL_NAME = {
        "ydiak": "Y Generáció Iskolaszövetkezet",
        "eudiakok": "euDIÁKOK",
        "schonherz": "Schönherz Iskolaszövetkezet"
    }

    name = models.TextField(
        unique=True,
        verbose_name="Szövetkezet neve"
    )

    def __str__(self):
            return self.PROVIDER_FULL_NAME.get(self.name, "Ismeretlen")

    class Meta:
        verbose_name = "Diákmunka Szövetkezet"
        verbose_name_plural = "Diákmunka Szövetkezetek"
