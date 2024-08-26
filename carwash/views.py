from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, CarModel, Price, Booking, Attendant, CarSize
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def create_booking(request):
    if request.method == "POST":
        car_model = get_object_or_404(CarModel, id=request.POST['car_model'])
        car_size = get_object_or_404(CarSize, id=request.POST['car_size'])
        booking = Booking.objects.create(
            customer=Customer.objects.get(user=request.user),
            car_model=car_model,
            car_size=car_size,
            car_make=car_model.make,
            confirmed=True
        )
        context = {
            'booking': booking,
            'cost': booking.get_cost(),
            'estimated_time': booking.get_estimated_time(),
        }
        return render(request, 'booking_confirmation.html', context)
    else:
        car_models = CarModel.objects.all()
        car_sizes = CarSize.objects.all()
        return render(request, 'create_booking.html', {'car_models': car_models, 'car_sizes': car_sizes})


@login_required
def admin_dashboard(request):
    bookings = Booking.objects.filter(confirmed=True, attendant__isnull=True)
    attendants = Attendant.objects.all()
    return render(request, 'admin_dashboard.html', {'bookings': bookings, 'attendants': attendants})


@login_required
def assign_attendant(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    attendant = get_object_or_404(Attendant, id=request.POST['attendant_id'])
    booking.attendant = attendant
    booking.save()
    return redirect('admin_dashboard')
