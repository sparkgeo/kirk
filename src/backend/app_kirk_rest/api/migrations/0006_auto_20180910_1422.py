# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-10 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180905_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='replicationjobs',
            name='destSchema',
            field=models.CharField(default='TEMP', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='replicationjobs',
            name='destTableName',
            field=models.CharField(default='TEMP', max_length=30),
            preserve_default=False,
        ),
    ]
