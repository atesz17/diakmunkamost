from django.db import models
from django.core.validators import URLValidator

from jobs.models import TimeStampedModel


class URL(TimeStampedModel):

    url = models.TextField(
        primary_key=True,
        validators=[URLValidator(schemes=['http', 'https'])],
        verbose_name='Munka URL címe'
    )
    state = models.ForeignKey(
        'State',
        on_delete=models.CASCADE,
        verbose_name="Scraping státusza"
    )


class State(TimeStampedModel):

    state = models.TextField(
        unique=True,
        verbose_name="Státusz"
    )
