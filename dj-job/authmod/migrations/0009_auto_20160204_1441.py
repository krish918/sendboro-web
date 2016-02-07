# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authmod', '0008_auto_20160123_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeHash',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('hash', models.CharField(max_length=255)),
                ('challenge', models.IntegerField(max_length=7, default=0)),
                ('phoneagent', models.CharField(null=True, max_length=512, default=None)),
                ('ts', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='rawuser',
            name='vericode',
        ),
    ]
