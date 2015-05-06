# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_auto_20150311_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phash',
            field=models.CharField(max_length=512),
            preserve_default=True,
        ),
    ]
