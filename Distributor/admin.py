from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(DistributorStock)
admin.site.register(DistributeToRetailer)
admin.site.register(DayByDayProductsDistributeToRetailer)
