# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-19 02:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20160325_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='end_ts',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='update_ts',
            field=models.DateTimeField(auto_now=True),
        ),
    ]