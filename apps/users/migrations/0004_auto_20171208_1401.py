# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-08 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20171207_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='img/batman.png', null=True, upload_to='media/img', verbose_name='头像'),
        ),
    ]
