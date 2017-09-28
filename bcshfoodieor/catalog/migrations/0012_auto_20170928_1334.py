# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 18:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0011_noterestaurant'),
    ]

    operations = [
        migrations.CreateModel(
            name='URRestaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('note', models.TextField(default='None', max_length=1000)),
                ('obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Restaurant', verbose_name='Restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'db_table': 'user_restaurant_sys',
            },
        ),
        migrations.AlterField(
            model_name='noterestaurant',
            name='note',
            field=models.TextField(default='None', max_length=1000),
        ),
    ]
