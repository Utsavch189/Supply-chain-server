from django.urls import path
from .views import *

urlpatterns = [
    path('get_stock',get_stock),
    path('receive_stock_history',receive_stock_history),
    path('distribute',distribute),
    path('post_dayBYdayDistribute',post_dayBYdayDistribute),
    path('get_dayBYdayDistribute',get_dayBYdayDistribute)
]