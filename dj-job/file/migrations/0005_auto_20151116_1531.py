# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0004_auto_20150418_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='author',
            field=models.ForeignKey(to='common.User', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
    ]
