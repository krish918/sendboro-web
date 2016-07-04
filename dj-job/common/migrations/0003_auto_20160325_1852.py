# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_usermobiledevice'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([('dialcode', 'phone')]),
        ),
    ]
