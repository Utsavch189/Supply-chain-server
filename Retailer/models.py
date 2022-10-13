from django.db import models
from datetime import date

class RetailerStock(models.Model):
    product_id=models.CharField(null=True,blank=True,max_length=30)
    product_name=models.CharField(null=True,blank=True,max_length=25)
    retailer_id=models.CharField(null=True,blank=True,max_length=25)
    distributor_id=models.CharField(null=True,blank=True,max_length=25)
    product_quantity=models.CharField(null=True,blank=True,max_length=20)
    total_price=models.CharField(null=True,blank=True,max_length=20)
    price_per_product=models.CharField(null=True,blank=True,max_length=10)
    date=models.DateField(date.today())

    def __str__(self):
        return '('+self.product_name+')'+' '+'( from:'+self.distributor_id+')'


class DistributeToCustomer(models.Model):
    retailer_id=models.CharField(null=True,blank=True,max_length=25)
    product_id=models.CharField(null=True,blank=True,max_length=30)
    product_quantity=models.CharField(null=True,blank=True,max_length=20)
    total_price=models.CharField(null=True,blank=True,max_length=20)
    calculation_status=models.BooleanField(default=False)
    date=models.DateField(date.today())

    def __str__(self):
        return '('+self.product_id+')'+' '+'( from:'+self.retailer_id+')'


class DayByDayProductsDistributeToCustomer(models.Model):
    product_id=models.CharField(null=True,blank=True,max_length=30)
    retailer_id=models.CharField(null=True,blank=True,max_length=25)
    product_quantity=models.CharField(null=True,blank=True,max_length=20)
    date=models.DateField(date.today())
    
    def __str__(self):
        return '('+self.product_id+')'+' '+'( from:'+self.retailer_id+')'
