# Generated by Django 3.2.11 on 2022-01-19 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0026_remove_item_max_loan_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='max_loan_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Maks lånevarighet (dager)'),
        ),
    ]
