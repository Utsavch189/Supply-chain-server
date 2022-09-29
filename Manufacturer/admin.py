from django.contrib import admin
from .models import SetProduct,ManufacturerStock,Distribute,DayByDayProducts

# Register your models here.
admin.site.register(SetProduct)
admin.site.register(ManufacturerStock)
admin.site.register(Distribute)
admin.site.register(DayByDayProducts)