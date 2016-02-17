from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Hozzáadás dátuma'
    )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Módosítás dátuma'
    )

    class Meta:
        abstract = True


class Job(TimeStampedModel):

    '''
    Parsing (es architekturalis) problemak miatt egyelore csak:
        1. Pesti munkakat jelenitek meg a honlapon (nem lehet mezore keresni)
        2. Munkaido is csak text (nem lehet mezore keresni)

    Kesobbi prioritas lesz majd ezen mezok rendes megvalositasa
    '''

    KONNYU_FIZIKAI = 0
    IRODAI = 1
    TELEFONOS = 2
    HOSTESS = 3
    MUSZAKI = 4
    INFORMATIKAI = 5
    ARUHAZI_VENDEGLATOS = 6
    EGYEB = 7

    JOB_TYPES = [
        (KONNYU_FIZIKAI, 'Könnyű fizikai'),
        (IRODAI, 'Irodai'),
        (TELEFONOS, 'Telefonos'),
        (HOSTESS, 'Hostess'),
        (MUSZAKI, 'Műszaki'),
        (INFORMATIKAI, 'Informatikai'),
        (ARUHAZI_VENDEGLATOS, 'Áruházi/Vendéglátós'),
        (EGYEB, 'Egyéb'),
    ]
    title = models.TextField(verbose_name='Munka megnevezése')
    job_type = models.IntegerField(
        choices=JOB_TYPES,
        db_index=True,
        verbose_name='Munka típusa'
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
        verbose_name='Munka URL címe'
    )
    other_info = models.TextField(blank=True, verbose_name='Egyéb információ')

    def get_absolute_url(self):
        return reverse('jobs:specific_job', args=(self.id,))

    '''
    Sajnos django nem allitja le a full_clean-t, ha a kulonbozo fieldeknel
    ValidationError volt, hanem megy tovabb, es egy dictbe beleteszi az
    errokat. Ezert 2x kell ellenorizni, hogy nem ures a min/max salary field
    (egyszer automatikusan a clean_field-nel, egyszer pedig a clean-ben)

    https://docs.djangoproject.com/en/1.9/_modules/django/db/models/base/#Model.full_clean
    '''

    def validate_min_max_salary(self):
        if self.min_salary is None or self.max_salary is None:
            raise ValidationError('Minimum órabér vagy maximum órabér üres')
        if self.min_salary > self.max_salary:
            msg = "min_salary({0}) cannot be greater than max_salary({1})"
            raise ValidationError(
                msg.format(self.min_salary, self.max_salary)
            )

    def clean(self):
        self.validate_min_max_salary()

    def __str__(self):
        return self.title
