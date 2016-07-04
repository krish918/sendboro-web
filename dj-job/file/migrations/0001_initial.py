# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.utils.general


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlindDelivery',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=100)),
                ('status', models.CharField(default='0', choices=[('0', 'stored'), ('1', 'moved')], max_length=1)),
                ('update_ts', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='0', choices=[('0', 'Reached Server'), ('1', 'Seen'), ('2', 'Downloaded'), ('3', 'Directlink'), ('4', 'Both')], max_length=1)),
                ('update_ts', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DirectUnsignedView',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('viewer_ip', models.CharField(max_length=16)),
                ('viewer_ua', models.CharField(max_length=512)),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('fileid', models.AutoField(unique=True, primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=255)),
                ('path', models.FileField(upload_to=common.utils.general.Helper.getFilePath, max_length=512)),
                ('size', models.CharField(max_length=10)),
                ('type', models.CharField(max_length=255, null=True)),
                ('sent_ts', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='common.User')),
                ('recievers', models.ManyToManyField(through='file.Delivery', to='common.User', related_name='Receiver')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='directunsignedview',
            name='file',
            field=models.ForeignKey(to='file.File'),
            preserve_default=True,
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
        migrations.AddField(
            model_name='blinddelivery',
            name='file',
            field=models.ForeignKey(to='file.File'),
            preserve_default=True,
        ),
    ]
