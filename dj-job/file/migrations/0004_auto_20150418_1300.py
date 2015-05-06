# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0003_file_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectUnsignedView',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('viewer_ip', models.CharField(max_length=16)),
                ('viewer_ua', models.CharField(max_length=512)),
                ('ts', models.DateTimeField(auto_now_add=True)),
                ('file', models.ForeignKey(to='file.File')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='blinddelivery',
            name='status',
            field=models.CharField(choices=[('0', 'stored'), ('1', 'moved')], default='0', max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='status',
            field=models.CharField(choices=[('0', 'Reached Server'), ('1', 'Seen'), ('2', 'Downloaded'), ('3', 'Directlink'), ('4', 'Both')], default='0', max_length=1),
            preserve_default=True,
        ),
    ]
