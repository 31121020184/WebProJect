# Generated by Django 5.1.1 on 2024-11-06 06:46

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_tintuc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tintuc',
            name='noi_dung',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]