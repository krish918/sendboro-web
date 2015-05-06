# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authmod', '0003_auto_20150311_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawuser',
            name='ipaddress',
            field=models.CharField(max_length=16, default=None, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rawuser',
            name='ts',
            field=models.DateTimeField(null=True, default=None, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rawuser',
            name='uastring',
            field=models.CharField(max_length=255, default=None, null=True),
            preserve_default=True,
        ),
    ]
