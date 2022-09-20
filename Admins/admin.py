from django.contrib import admin
from .models import ApprovedUsers,DeletedUsers

admin.site.register(ApprovedUsers)
admin.site.register(DeletedUsers)

# Register your models here.
