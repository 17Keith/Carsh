from rest_framework import serializers
from .models import Customer, CarModel, Price, Booking, Attendant


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "phone_number"]


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = "__all__"


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class AttendantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendant
        fields = ["id", "name", "bookings"]
