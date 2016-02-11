# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodeHash',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=255)),
                ('challenge', models.IntegerField(default=0, max_length=7)),
                ('responseagent', models.CharField(default=None, max_length=512, null=True)),
                ('requestip', models.CharField(default=None, max_length=16, null=True)),
                ('requestagent', models.CharField(default=None, max_length=512, null=True)),
                ('resolve_status', models.BooleanField(default=False)),
                ('mitigate', models.BooleanField(default=False)),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RawUser',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(unique=True, max_length=16)),
                ('attempt', models.IntegerField(default=1)),
                ('uastring', models.CharField(default=None, max_length=512, null=True)),
                ('ipaddress', models.CharField(default=None, max_length=16, null=True)),
                ('ts', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
