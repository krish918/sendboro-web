# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.utils.general


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_auto_20150403_0348'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('status', models.CharField(max_length=1, default='0')),
                ('update_ts', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('fileid', models.AutoField(serialize=False, unique=True, primary_key=True)),
                ('filename', models.CharField(max_length=255)),
                ('path', models.FileField(upload_to=common.utils.general.Helper.getFilePath)),
                ('size', models.IntegerField()),
                ('sent_ts', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='common.User', related_name='Author')),
                ('recievers', models.ManyToManyField(through='file.Delivery', to='common.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='delivery',
            name='file',
            field=models.ForeignKey(to='file.File'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='delivery',
            name='user',
            field=models.ForeignKey(to='common.User'),
            preserve_default=True,
        ),
    ]
