# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-15 02:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='res_id',
            new_name='res',
        ),
    ]
