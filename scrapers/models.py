from django.db import models
from django.core.validators import URLValidator

from helpers.models import TimeStampedModel


class URL(TimeStampedModel):
    """
    A scrapelt diakmunkahoz tartozo alapadatok.

    url -- Ezen az url-en talalhato meg a munka
    state -- scrapeles allapota (siker, kudarc)
    provider -- diakszovetkezet neve
    scraped_data -- json-ba rakja bele a leszedett adatokat
    """

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

    provider = models.ForeignKey(
        'Provider',
        on_delete=models.CASCADE,
        verbose_name="Diakszövetkezet rövid neve"
    )

    scraped_data = models.TextField(
        verbose_name="Scrapelt JSON"
    )

    def __str__(self):
        if self.url[-1] == "/":
            s = str(self.url).split("/")
            return s[-2]
        else:
            return str(self.url).split("/")[-1]


class State(TimeStampedModel):
    """
    Scraping statuszt reprezentalo osztaly.
    """

    state = models.TextField(
        unique=True,
        verbose_name="Státusz"
    )

    def __str__(self):
        return self.state


class Provider(TimeStampedModel):
    """
    Diakszovetkezet.
    """

    name = models.TextField(
        verbose_name="Diakszövetkezet rövid neve"
    )

    def __str__(self):
        return self.name