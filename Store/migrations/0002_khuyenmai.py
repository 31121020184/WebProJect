# Generated by Django 5.1.1 on 2024-10-29 06:40

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KhuyenMai',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.FloatField()),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField()),
                ('san_pham', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.sanpham')),
            ],
        ),
    ]