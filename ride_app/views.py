from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from .models import *
from users.models import Profile
import stripe
from django.contrib.auth.decorators import login_required

stripe.api_key = "sk_test_51HZrGTHxxr6MhWwJONOeO5JOlj51IqJFPna0vIgjgog59OdkhepxOJsXRzCex18vmOQuz14MiXagYLGhdXRdD1eP00Itvri0tI"


@login_required(login_url='index')
def home(request):
    context = {
        'this_user': User.objects.get(id=request.user.id),
        'rides': Ride.objects.all(),
        'other_users': Ride.objects.exclude(created_by=request.user.id)
    }
    return render(request, "Ride_app/rides.html", context)


@login_required(login_url='index')
def create_ride(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.created_by = request.user
            ride.save()
            return redirect('ride_app:home')
    else:
        form = RideForm()

    return render(request, 'ride_app/add_ride.html', {'form': form})


@login_required(login_url='index')
def update_ride(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    if request.method == 'POST':
        form = RideForm(request.POST, instance=ride)
        if form.is_valid():
            form.save()
            return redirect('ride_app:home')
    else:
        form = RideForm(instance=ride)
    return render(request, 'ride_app/edit_ride.html', {'form': form})


@login_required(login_url='index')
def ride(request, ride_id):
    context = {
        'ride': Ride.objects.get(id=ride_id),
        'joiners': User.objects.filter(joined_rides=ride_id)
    }
    return render(request, 'Ride_app/ride.html', context)


@login_required(login_url='index')
def join_ride(request, ride_id):
    user = request.user
    ride = Ride.objects.get(id=ride_id)
    ride.joined_by.add(user)

    return redirect("ride_app:home")


@login_required(login_url='index')
def cancel_ride(request, ride_id):
    user = request.user
    ride = Ride.objects.get(id=ride_id)
    ride.joined_by.remove(user)
    return redirect("ride_app:home")


@login_required(login_url='index')
def delete_ride(request, ride_id):
    to_delete = Ride.objects.get(id=ride_id)
    to_delete.delete()
    return redirect("ride_app:home")


@login_required(login_url='index')
def charge(request):
    if request.method == 'POST':
        print('Data:', request.POST)

        amount = int(request.POST['amount'])

        customer = stripe.Customer.create(
            email=request.POST['email'],
            source=request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='usd',
            description='Payment'
        )
    return redirect("ride_app:home")
