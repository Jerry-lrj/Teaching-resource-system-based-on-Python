# -*- coding: utf-8 -*-
# Generated by Django source.11.14 on 2019-03-23 09:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bysj', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='booklist',
            unique_together=set([('course', 'userinfos')]),
        ),
    ]
