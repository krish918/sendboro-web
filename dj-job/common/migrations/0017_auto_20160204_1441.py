# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0016_auto_20160128_1031'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='ts',
            new_name='start_ts',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phash',
        ),
        migrations.AddField(
            model_name='session',
            name='end_ts',
            field=models.DateTimeField(auto_now=True, default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='countrycode',
            field=models.CharField(max_length=4, default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.BigIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='update_ts',
            field=models.DateTimeField(auto_now=True, default=None),
            preserve_default=True,
        ),
    ]
