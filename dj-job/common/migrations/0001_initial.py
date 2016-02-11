# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('sessionid', models.AutoField(unique=True, primary_key=True, serialize=False)),
                ('uastring', models.CharField(max_length=512)),
                ('ipaddress', models.CharField(max_length=16)),
                ('active', models.BooleanField(default=True)),
                ('start_ts', models.DateTimeField(auto_now_add=True)),
                ('end_ts', models.DateTimeField(default=None, auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.AutoField(unique=True, primary_key=True, serialize=False)),
                ('dialcode', models.CharField(max_length=8)),
                ('phone', models.BigIntegerField()),
                ('countrycode', models.CharField(default=None, max_length=4)),
                ('username', models.CharField(unique=True, default=None, max_length=16, null=True)),
                ('fullname', models.CharField(default=None, max_length=255, null=True)),
                ('account_ts', models.DateTimeField(auto_now_add=True)),
                ('update_ts', models.DateTimeField(default=None, auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(to='common.User'),
            preserve_default=True,
        ),
    ]
