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