# Generated by Django 2.0.9 on 2018-10-03 21:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slots', models.IntegerField()),
                ('term', models.CharField(max_length=20)),
                ('start_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TimeTableSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('day', models.IntegerField()),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.TimeTable')),
            ],
        ),
        migrations.CreateModel(
            name='TimeTableSlotSignup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_table_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internal.TimeTableSlot')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
