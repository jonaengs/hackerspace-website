# Generated by Django 2.0.9 on 2018-10-10 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timetableslotsignup',
            options={'permissions': (('admin_office_hours', 'Can admin office hours'),)},
        ),
    ]
