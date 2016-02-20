# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-20 19:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_auto_20160217_2357'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Szövetkezet neve')),
            ],
            options={
                'verbose_name': 'Diákmunka Szövetkezet',
            },
        ),
        migrations.AlterModelOptions(
            name='job',
            options={'verbose_name': 'Diákmunka'},
        ),
    ]