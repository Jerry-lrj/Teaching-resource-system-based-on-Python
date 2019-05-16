# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-04-23 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bysj', '0010_annunciate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='roles',
            field=models.ManyToManyField(blank=True, null=True, to='bysj.Role', verbose_name='用户拥有的权限'),
        ),
    ]
