from .views import *
from django.urls import path

urlpatterns = [
    path('login',login),
    path('createuser',createuser),
    path('sendotp',sendotp),
    path('resetpassword',resetpassword),
    path('sendotp_middlereg',sendotp_middlereg),
    path('verify_middlereg',verify_middlereg),
    path('refresh_token',refresh_token),
    path('is_block',is_block),
]