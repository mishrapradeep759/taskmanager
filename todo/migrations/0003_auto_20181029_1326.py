# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-29 13:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20181026_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]
