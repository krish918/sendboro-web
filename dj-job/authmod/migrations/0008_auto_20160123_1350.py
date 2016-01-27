# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authmod', '0007_auto_20150418_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawuser',
            name='ts',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rawuser',
            name='vericode',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
