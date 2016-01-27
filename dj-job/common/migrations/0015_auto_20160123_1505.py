# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_auto_20150403_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='countrycode',
            field=models.CharField(max_length=8),
            preserve_default=True,
        ),
    ]
