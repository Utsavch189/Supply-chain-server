from django.urls import path
from .views import *

urlpatterns = [
    path('requests',requests),
    path('approved_users',approved_users),
    path('deletedusers_users',deletedusers_users),
    path('approve_a_user',approve_a_user),
    path('delete_a_user',delete_a_user),
    path('reapprove_a_user',reapprove_a_user),
    path('numbers_of_users',numbers_of_users)
]