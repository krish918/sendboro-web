# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0011_auto_20150312_0127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commences',
            name='session',
        ),
        migrations.RemoveField(
            model_name='commences',
            name='user',
        ),
        migrations.DeleteModel(
            name='Commences',
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(to='common.User', default=0),
            preserve_default=True,
        ),
    ]
