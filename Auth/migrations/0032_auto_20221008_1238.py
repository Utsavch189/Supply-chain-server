# Generated by Django 3.2.8 on 2022-10-08 07:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0031_auto_20221007_2033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='created_at',
        ),
        migrations.AddField(
            model_name='otp',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='otp',
            name='created_at_date',
            field=models.TimeField(default=datetime.time(12, 38, 43, 877593)),
        ),
        migrations.AlterField(
            model_name='register',
            name='created_at',
            field=models.DateField(verbose_name=datetime.date(2022, 10, 8)),
        ),
    ]
