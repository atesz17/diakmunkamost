# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-28 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20160128_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='other_info',
            field=models.TextField(blank=True, verbose_name='Egyéb információ'),
        ),
        migrations.AlterField(
            model_name='job',
            name='place_of_work',
            field=models.TextField(verbose_name='Munkavégzés helye'),
        ),
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.TextField(verbose_name='Munka megnevezése'),
        ),
        migrations.AlterField(
            model_name='job',
            name='url',
            field=models.TextField(verbose_name='Munka URL címe'),
        ),
        migrations.AlterField(
            model_name='job',
            name='working_hours',
            field=models.TextField(verbose_name='Munkaidő'),
        ),
    ]
