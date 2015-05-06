# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150311_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='ts',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
