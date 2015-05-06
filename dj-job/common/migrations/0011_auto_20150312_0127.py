# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_auto_20150311_1516'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commences',
            old_name='sessionid',
            new_name='session',
        ),
        migrations.RenameField(
            model_name='commences',
            old_name='userid',
            new_name='user',
        ),
    ]
