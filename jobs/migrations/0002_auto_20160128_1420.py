# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-28 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_squashed_0008_auto_20160127_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Hozzáadás dátuma'),
        ),
        migrations.AlterField(
            model_name='job',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Módosítás dátuma'),
        ),
        migrations.AlterField(
            model_name='job',
            name='url',
            field=models.CharField(max_length=250, verbose_name='Munka URL címe'),
        ),
    ]
