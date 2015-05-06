# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20150311_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phash',
            field=models.CharField(max_length=128),
            preserve_default=True,
        ),
    ]
