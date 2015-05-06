# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.utils.general


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlindDelivery',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('phone', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('0', 'Reached Server'), ('1', 'Seen'), ('2', 'Downloading'), ('3', 'Delivered')], max_length=1, default='0')),
                ('update_ts', models.DateTimeField(auto_now=True)),
                ('file', models.ForeignKey(to='file.File')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='status',
            field=models.CharField(choices=[('0', 'Reached Server'), ('1', 'Seen'), ('2', 'Downloading'), ('3', 'Delivered')], max_length=1, default='0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='author',
            field=models.ForeignKey(to='common.User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='path',
            field=models.FileField(max_length=512, upload_to=common.utils.general.Helper.getFilePath),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='recievers',
            field=models.ManyToManyField(through='file.Delivery', to='common.User', related_name='Receiver'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='size',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]
