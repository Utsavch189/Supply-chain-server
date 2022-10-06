from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(RetailerStock)
admin.site.register(DistributeToCustomer)
admin.site.register(DayByDayProductsDistributeToCustomer)