# Generated by Django 2.0.10 on 2019-03-21 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0002_auto_20181010_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='term',
            field=models.CharField(max_length=3, unique=True),
        ),
    ]
