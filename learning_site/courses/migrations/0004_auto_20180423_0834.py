# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-22 23:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0003_auto_20180419_1953'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Step',
            new_name='Text',
        ),
    ]
