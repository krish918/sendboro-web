# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_auto_20150403_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='user',
            field=models.ForeignKey(to='common.User', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
    ]
