# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-17 15:44
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_auto_20160202_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='url',
            field=models.TextField(validators=[django.core.validators.URLValidator(schemes=['http', 'https'])], verbose_name='Munka URL címe'),
        ),
    ]
