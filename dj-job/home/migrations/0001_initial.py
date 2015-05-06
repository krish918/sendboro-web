# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_auto_20150403_0348'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('picid', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('large', models.ImageField(upload_to='photo/user/%Y/%m/%d')),
                ('med', django_resized.forms.ResizedImageField(upload_to='photo/user/%Y/%m/%d')),
                ('small', django_resized.forms.ResizedImageField(upload_to='photo/user/%Y/%m/%d')),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to='common.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
