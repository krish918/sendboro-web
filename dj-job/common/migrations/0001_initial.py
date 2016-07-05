# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 03:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('sessionid', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('uastring', models.CharField(max_length=512)),
                ('ipaddress', models.CharField(max_length=16)),
                ('active', models.BooleanField(default=True)),
                ('start_ts', models.DateTimeField(auto_now_add=True)),
                ('end_ts', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('dialcode', models.CharField(max_length=8)),
                ('phone', models.BigIntegerField()),
                ('countrycode', models.CharField(default=None, max_length=4)),
                ('username', models.CharField(default=None, max_length=16, null=True, unique=True)),
                ('fullname', models.CharField(default=None, max_length=255, null=True)),
                ('account_ts', models.DateTimeField(auto_now_add=True)),
                ('update_ts', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserMobileDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneagent', models.CharField(max_length=512)),
                ('ts', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.User')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([('dialcode', 'phone')]),
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.User'),
        ),
    ]
