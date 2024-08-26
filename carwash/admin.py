from django.contrib import admin
from .models import Customer, CarModel, Price, Booking, Attendant, CarSize, EstimatedTime

admin.site.register(Customer)
admin.site.register(CarModel)
admin.site.register(Price)
admin.site.register(Booking)
admin.site.register(Attendant)
admin.site.register(CarSize)
admin.site.register(EstimatedTime)