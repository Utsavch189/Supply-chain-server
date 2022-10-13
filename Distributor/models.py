from django.db import models
from datetime import date

class DistributorStock(models.Model):
    product_id=models.CharField(null=True,blank=True,max_length=30)
    product_name=models.CharField(null=True,blank=True,max_length=25)
    manufacturer_id=models.CharField(null=True,blank=True,max_length=25)
    distributor_id=models.CharField(null=True,blank=True,max_length=50)
    product_quantity=models.CharField(null=True,blank=True,max_length=20)
    total_price=models.CharField(null=True,blank=True,max_length=20)
    price_per_product=models.CharField(null=True,blank=True,max_length=10)
    date=models.DateField(date.today())

    def __str__(self):
        return '('+self.product_name+')'+' '+'( from:'+self.manufacturer_id+')'


class DistributeToRetailer(models.Model):
    retailer_id=models.CharField(null=True,blank=True,max_length=25)
    product_id=models.CharField(null=True,blank=True,max_length=30)
    distributor_id=models.CharField(null=True,blank=True,max_length=25)
    product_quantity=models.CharField(null=True,blank=True,max_length=20)
    total_price=models.CharField(null=True,blank=True,max_length=20)
    calculation_status=models.BooleanField(default=False)
    date=models.DateField(date.today())

    def __str__(self):
        return '('+self.product_id+')'+' '+'( from:'+self.distributor_id+')'


class DayByDayProductsDistributeToRetailer(models.Model):
    product_id=models.CharField(null=True,blank=True,max_length=30)
    retailer_id=models.CharField(null=True,blank=True,max_length=50)
    product_quantity=models.CharField(null=True,blank=True,max_length=10)
    distributor_id=models.CharField(null=True,blank=True,max_length=50)
    date=models.DateField(date.today())
    
    def __str__(self):
        return '('+self.product_id+')'+' '+'( from:'+self.distributor_id+')'
