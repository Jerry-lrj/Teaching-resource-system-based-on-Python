# -*- coding: utf-8 -*-
# Generated by Django source.11.14 on 2019-03-27 13:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bysj', '0004_userinfo_birthday'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=32, verbose_name='权限')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='角色名称')),
                ('permission', models.ManyToManyField(to='bysj.Permission', verbose_name='角色拥有权限')),
            ],
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='birthday',
            field=models.DateField(verbose_name='生日'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='roles',
            field=models.ManyToManyField(to='bysj.Role', verbose_name='用户拥有的权限'),
        ),
    ]
