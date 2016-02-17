from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Hozzáadás dátuma')
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Módosítás dátuma')

    class Meta:
        abstract = True


class Job(TimeStampedModel):
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
        verbose_name='Munka típusa')
    '''
    ezt majd max kesobb, most nem prioritas, hogy lehessen keresni
    hely alapjan. A problema, hogy listaban kene lennie, hiszen van
    olyan melo, amit tobb helyen lehet vegezni...
    Egyelore legyen az a terv, hogy
    CSAK PESTI!!!!!!
    melokat fogunk kilistazni
    '''
    task = models.TextField(verbose_name='Feladat leírása')
    place_of_work = models.TextField(verbose_name='Munkavégzés helye')
    min_salary = models.IntegerField(
        db_index=True, verbose_name='Minumum órabér')
    max_salary = models.IntegerField(verbose_name='Maximum órabér')
    '''
    itt is hasonlo a helyzet, mint a job_type-nal
    vagyis van olyan, hogy tobb erteket adnak meg, valahol pontos
    intervallumot irnak le, mashol orat, szval nehezkes, Egyelore
    nem prioritas
    '''
    working_hours = models.TextField(verbose_name='Munkaidő')
    requirements = models.TextField(verbose_name='Feltételek')
    url = models.TextField(
        validators=[URLValidator(schemes=['http', 'https'])],
        verbose_name='Munka URL címe')
    other_info = models.TextField(blank=True, verbose_name='Egyéb információ')

    def get_absolute_url(self):
        return reverse('jobs:specific_job', args=(self.id,))

    def check_max_salary_is_greater_or_equal_than_min_salary(self):
        if self.min_salary > self.max_salary:
            msg = "min_salary({0}) cannot be greater than max_salary({1})"
            raise ValidationError(
                msg.format(self.min_salary, self.max_salary))

    '''
    Azert hulyeseg ez a fgv, mert django alapbol nem engedne ures fielddel
    elmenteni oket, viszont django-admin-nal kiakad, ha nem ellenorzom elotte
    hogy nem uresek a fieldek. TODO: valami jobb megoldas
    '''
    def check_for_None_types_in_min_and_max_salary(self):
        if self.min_salary is None or self.max_salary is None:
            raise ValidationError('Minimum órabér vagy maximum órabér üres')

    def validate_min_max_salary(self):
        # Ehelyett kene valami jobbat kitalalni
        self.check_for_None_types_in_min_and_max_salary()
        self.check_max_salary_is_greater_or_equal_than_min_salary()

    '''
    Ez egy eleg bena workaround, a cel az lenne, hogy min<=max MINDIG. Eddig
    csak <= check volt, testeken at is ment, viszont admin felulet kiakadt,
    mert None volt mindketto, ha nem irtam bele semmit.
    '''
    def clean(self):
        self.validate_min_max_salary()

    def __str__(self):
        return self.title
