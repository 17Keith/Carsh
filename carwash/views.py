from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, Attendant
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request, 'base.html')


def logout_view(request):
    auth_logout(request)
    return redirect('index')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def book_carwash(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            car_size = form.cleaned_data['car_size']
            if car_size == 'small':
                booking.price = 300
                booking.time_estimate = '30 Minutes'
            elif car_size == 'medium':
                booking.price = 500
                booking.time_estimate = '45 minutes'
            elif car_size == 'large':
                booking.price = 700
                booking.time_estimate = '1 hour'
            booking.save()
            return redirect('index')
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form})


def booking_list(request):
    bookings = Booking.objects.all()
    attendants = ['Attendant 1', 'Attendant 2', 'Attendant 3']
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        attendant_name = request.POST.get('attendant')
        booking = Booking.objects.get(id=booking_id)
        booking.attendant = attendant_name
        booking.save()
        return redirect('booking_list')
    return render(request, 'booking_list.html', {'bookings': bookings, 'attendants': attendants})


@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    estimated_time = booking.get_estimated_time()
    total_cost = booking.get_total_cost()

    context = {
        'booking': booking,
        'estimated_time': estimated_time,
        'total_cost': total_cost,
    }
    return render(request, 'booking_confirmation.html', context)


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
