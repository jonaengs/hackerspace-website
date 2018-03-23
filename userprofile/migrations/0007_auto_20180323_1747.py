# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-23 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_auto_20180309_2215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='auto_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
        migrations.AlterField(
            model_name='profile',
            name='group',
            field=models.ManyToManyField(blank=True, related_name='profile', to='userprofile.Group', verbose_name='Gruppe'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default=None, upload_to='profilepictures', verbose_name='Profilbilde'),
        ),
    ]
