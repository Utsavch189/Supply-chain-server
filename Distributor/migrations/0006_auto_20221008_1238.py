# Generated by Django 3.2.8 on 2022-10-08 07:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Distributor', '0005_auto_20221007_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daybydayproductsdistributetoretailer',
            name='date',
            field=models.DateField(verbose_name=datetime.date(2022, 10, 8)),
        ),
        migrations.AlterField(
            model_name='distributetoretailer',
            name='date',
            field=models.DateField(verbose_name=datetime.date(2022, 10, 8)),
        ),
        migrations.AlterField(
            model_name='distributorstock',
            name='date',
            field=models.DateField(verbose_name=datetime.date(2022, 10, 8)),
        ),
    ]
