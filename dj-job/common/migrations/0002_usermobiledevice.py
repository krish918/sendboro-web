# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMobileDevice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('phoneagent', models.CharField(max_length=512)),
                ('ts', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to='common.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
