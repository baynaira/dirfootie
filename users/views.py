from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.db import IntegrityError

def redirect_to_login(request):
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect('store:product_list')
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'users/login.html')

def signup_view(request):
    if request.method == 'POST':
        fullname = request.POST.get('full_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if any of the fields are empty
        if not fullname or not username or not password:
            error_message = "All fields are required. Please fill out the form completely."
            return render(request, 'users/signup.html', {'error': error_message})

        try:
            # Attempt to create the user
            user = User.objects.create_user(username=username, password=password, first_name=fullname)
            auth_login(request, user)
            request.session['username'] = username
            return redirect('store:product_list')
        except IntegrityError:
            # Handle the case where the username is already taken
            error_message = "Username already exists. Please choose a different one."
            return render(request, 'users/signup.html', {'error': error_message})
        except ValueError:
            # Handle any other value errors (e.g., empty username)
            error_message = "Invalid credentials. Please try again."
            return render(request, 'users/signup.html', {'error': error_message})

    return render(request, 'users/signup.html')





