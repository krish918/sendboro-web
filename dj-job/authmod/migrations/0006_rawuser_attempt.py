# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authmod', '0005_auto_20150311_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawuser',
            name='attempt',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
