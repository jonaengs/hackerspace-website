# Generated by Django 2.0.10 on 2019-04-30 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seasonal_events', '0007_auto_20190318_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='banner_color',
            field=models.CharField(default='hs-green', help_text='Tar en CSS klasse til bakgrunnsfarge. Dette kan være for eksempel hs-green, hs-yellow, hs-red, etc.', max_length=50, verbose_name='bannertext'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='season',
            name='banner_text',
            field=models.CharField(default='hei', help_text='Tekst som vil vises i en banner på forsiden.', max_length=220, verbose_name='bannertext'),
            preserve_default=False,
        ),
    ]
