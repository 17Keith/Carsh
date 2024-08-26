from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('book/', views.book_carwash, name='book_carwash'),
    path('booking_list/', views.booking_list, name='booking_list'),
    path('confirm_booking/<int:booking_id>/',
         views.confirm_booking, name='confirm_booking'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('assign_attendant/<int:booking_id>/',
         views.assign_attendant, name='assign_attendant'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
]
