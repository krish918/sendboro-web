# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0015_auto_20160123_1505'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='countrycode',
            new_name='dialcode',
        ),
    ]
