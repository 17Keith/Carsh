from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Models for user(anyone who is interacting with the app, and wants to book in their car for a wash), Review and Pricing


class CarSize(models.Model):
    SIZE_CHOICES = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    ]

    size = models.CharField(max_length=20, choices=SIZE_CHOICES, unique=True)

    def __str__(self):
        return self.size


class EstimatedTime(models.Model):
    size = models.OneToOneField(CarSize, on_delete=models.CASCADE)
    time_minutes = models.IntegerField()

    def __str__(self):
        return f"{self.size.size} - {self.time_minutes} minutes"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=15)
    # User sets whether the car is a Small, Medium or a Large.
    size = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.make} {self.model} ({self.size})"

    # Price is dependent on the the size of the car! For a small car (Honda Fit, Alto, Golf and such) it can be 300/
    # Medium can be 400 (Any SUV)
    # Large can be 450 or 500


class Price(models.Model):
    SMALL = 'Small'
    MEDIUM = 'Medium'
    LARGE = 'Large'

    SIZE_CHOICES = [
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large')
    ]

    SMALL_COST = 300
    MEDIUM_COST = 500
    LARGE_COST = 700

    size = models.CharField(max_length=10, choices=SIZE_CHOICES, unique=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.size == self.SMALL:
            self.cost = self.SMALL_COST
        elif self.size == self.MEDIUM:
            self.cost = self.MEDIUM_COST
        elif self.size == self.LARGE:
            self.cost = self.LARGE_COST
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.size} : Ksh {self.cost}"


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    car_make = models.CharField(max_length=50)
    car_size = models.ForeignKey(CarSize, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    attendant = models.ForeignKey(
        'Attendant', on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_bookings")

    def get_estimated_time(self):
        return EstimatedTime.objects.get(size=self.car_size).time_minutes
    
    def get_cost(self):
        return Price.objects.get(size=self.car_model.size).cost

    def __str__(self):
        return f"Booking for {self.customer.username} - {self.car_make} {self.car_model}"

class Attendant(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
