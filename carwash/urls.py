from django.urls import path
from . import views

urlpatterns = [
    path('Customer/', views.Customer, name='customer'),
    path('pricing/', views.Price, name='pricing'),
    ]
