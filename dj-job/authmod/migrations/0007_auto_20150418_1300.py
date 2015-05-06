# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authmod', '0006_rawuser_attempt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawuser',
            name='uastring',
            field=models.CharField(null=True, default=None, max_length=512),
            preserve_default=True,
        ),
    ]
