from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            form = UserRegisterForm()
            login_form = AuthenticationForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse('ride_app:home'))
            else:
                messages.error(request, 'Username or Password is incorrect')
                return redirect('/')

        elif 'register' in request.POST:
            login_form = AuthenticationForm()
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                return redirect(reverse('ride_app:home'))
            else:
                messages.error(request, 'Inputs are invalid')
                return redirect('/')

    else:
        form = UserRegisterForm()
        login_form = AuthenticationForm()

    context = {
        'login_form': login_form,
        'form': form,
    }
    return render(request, 'users/index.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/index')
    else:
        form = UserRegisterForm()
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}')
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'ride_app/rides.html')

        return render(request, 'users/register.html', {'form': form})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/index')
            else:
                messages.info(request, 'Username or Password is incorrect')
        context = {}
        return render(request, 'users/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')
