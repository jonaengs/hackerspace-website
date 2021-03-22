# Generated by Django 3.1.2 on 2021-03-22 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20210322_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='site',
            field=models.CharField(default='*', help_text="Det interne navnet på URL-stien til sidene som banneret skal dukke opp på. Separert med komma (,). Wildcard (*) støttes. F.eks. er '*' ALLE sider, 'inventory:*' er alle lagersider.", max_length=250, verbose_name='bannersider'),
        ),
    ]
