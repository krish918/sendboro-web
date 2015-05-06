# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20150311_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phash',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
