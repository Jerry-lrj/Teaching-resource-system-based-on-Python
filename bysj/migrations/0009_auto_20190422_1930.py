# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-04-22 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bysj', '0008_user_liuyan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_liuyan',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bysj.UserInfo'),
        ),
    ]