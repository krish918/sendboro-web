# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('sessionid', models.AutoField(serialize=False, unique=True, primary_key=True)),
                ('uastring', models.CharField(max_length=512)),
                ('ipaddress', models.CharField(max_length=16)),
                ('active', models.BooleanField(default=True)),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.AutoField(serialize=False, unique=True, primary_key=True)),
                ('countrycode', models.CharField(max_length=4)),
                ('phone', models.BigIntegerField(unique=True)),
                ('username', models.CharField(null=True, max_length=16)),
                ('phash', models.CharField(max_length=50)),
                ('fullname', models.CharField(null=True, max_length=255)),
                ('account_ts', models.DateTimeField(auto_now_add=True)),
                ('update_ts', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='commences',
            name='sessionid',
            field=models.ForeignKey(to='common.Session'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commences',
            name='userid',
            field=models.ForeignKey(to='common.User'),
            preserve_default=True,
        ),
    ]
