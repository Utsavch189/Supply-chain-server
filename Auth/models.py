from email.policy import default

from django.db import models
from datetime import date,datetime

class Register(models.Model):
    name=models.CharField(null=True,blank=True,max_length=40)
    phone=models.CharField(null=True,blank=True,max_length=15)
    email=models.CharField(null=True,blank=True,max_length=40)
    password=models.CharField(null=True,blank=True,max_length=256)
    gender=models.CharField(null=True,blank=True,max_length=6)
    whatsapp_no=models.CharField(null=True,blank=True,max_length=15)
    role=models.CharField(null=True,blank=True,max_length=15)
    id_no=models.CharField(null=True,blank=True,max_length=25)
    created_at=models.DateField(date.today())


    
    def __str__(self):
        return self.name


class OTP(models.Model):
    target=models.CharField(null=True,blank=True,max_length=40)
    otp=models.CharField(null=True,blank=True,max_length=4)
    typed=models.CharField(null=True,blank=True,max_length=30)
    tried=models.IntegerField(null=True,blank=True,default=0)
    blocked=models.BooleanField(default=False)
    created_at_date=models.DateField(default=date.today())
    created_at_time=models.TimeField(default=datetime.now().time())