from django.db import models
from datetime import date,datetime

class ApprovedUsers(models.Model):
    name=models.CharField(null=True,blank=True,max_length=40)
    phone=models.CharField(null=True,blank=True,max_length=12)
    email=models.CharField(null=True,blank=True,max_length=40)
    password=models.CharField(null=True,blank=True,max_length=6)
    gender=models.CharField(null=True,blank=True,max_length=6)
    whatsapp_no=models.CharField(null=True,blank=True,max_length=12)
    role=models.CharField(null=True,blank=True,max_length=15)
    id_no=models.CharField(null=True,blank=True,max_length=25)
    approved_at=models.DateField(date.today())

    def __str__(self):
        return self.name


class DeletedUsers(models.Model):
    name=models.CharField(null=True,blank=True,max_length=40)
    phone=models.CharField(null=True,blank=True,max_length=12)
    email=models.CharField(null=True,blank=True,max_length=40)
    password=models.CharField(null=True,blank=True,max_length=6)
    gender=models.CharField(null=True,blank=True,max_length=6)
    whatsapp_no=models.CharField(null=True,blank=True,max_length=12)
    role=models.CharField(null=True,blank=True,max_length=15)
    id_no=models.CharField(null=True,blank=True,max_length=25)
    deleted_at=models.DateField(date.today())

    def __str__(self):
        return self.name