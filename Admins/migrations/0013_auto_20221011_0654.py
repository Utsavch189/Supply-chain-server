# Generated by Django 3.2.8 on 2022-10-11 01:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admins', '0012_auto_20221008_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvedusers',
            name='approved_at',
            field=models.DateField(verbose_name=datetime.date(2022, 10, 11)),
        ),
        migrations.AlterField(
            model_name='deletedusers',
            name='deleted_at',
            field=models.DateField(verbose_name=datetime.date(2022, 10, 11)),
        ),
    ]
