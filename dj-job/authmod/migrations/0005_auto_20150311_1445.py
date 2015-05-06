# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authmod', '0004_auto_20150311_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawuser',
            name='ts',
            field=models.DateTimeField(null=True, auto_now=True, default=None),
            preserve_default=True,
        ),
    ]
