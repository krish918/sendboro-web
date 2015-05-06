# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authmod', '0002_auto_20150311_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawuser',
            name='ipaddress',
            field=models.CharField(default=None, max_length=16),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rawuser',
            name='ts',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rawuser',
            name='uastring',
            field=models.CharField(default=None, max_length=255),
            preserve_default=True,
        ),
    ]
