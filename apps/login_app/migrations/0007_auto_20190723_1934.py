# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-24 02:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0006_auto_20190723_1844'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Otrip',
        ),
        migrations.RemoveField(
            model_name='user',
            name='otrip',
        ),
    ]
