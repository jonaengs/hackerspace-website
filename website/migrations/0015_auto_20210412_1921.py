# Generated by Django 3.1.1 on 2021-04-12 19:21

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_auto_20210412_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
