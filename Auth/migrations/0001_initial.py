# Generated by Django 3.2.8 on 2022-10-13 06:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(blank=True, max_length=46, null=True)),
                ('otp', models.CharField(blank=True, max_length=4, null=True)),
                ('typed', models.CharField(blank=True, max_length=30, null=True)),
                ('tried', models.IntegerField(blank=True, default=0, null=True)),
                ('blocked', models.BooleanField(default=False)),
                ('created_at_date', models.DateField(verbose_name=datetime.date(2022, 10, 13))),
                ('created_at_time', models.TimeField(verbose_name=datetime.time(11, 46, 3, 71824))),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.CharField(blank=True, max_length=46, null=True)),
                ('password', models.CharField(blank=True, max_length=256, null=True)),
                ('gender', models.CharField(blank=True, max_length=6, null=True)),
                ('whatsapp_no', models.CharField(blank=True, max_length=15, null=True)),
                ('role', models.CharField(blank=True, max_length=15, null=True)),
                ('id_no', models.CharField(blank=True, max_length=25, null=True)),
                ('created_at', models.DateField(verbose_name=datetime.date(2022, 10, 13))),
            ],
        ),
    ]
