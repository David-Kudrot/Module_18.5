from django.shortcuts import render, redirect
from user.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            return redirect('login')
    else:
        signup_form = SignupForm()
    return render(request, 'signup.html', {'form': signup_form})


def log_in(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                messages.success(request, "Logged In Successfully")
                login(request, user)
                return redirect('profile')
            else:
                messages.warning(request, "Wrong username or password")
                return redirect('login')
        else:
            messages.warning(request, "Username or Password is incorrect")
            return redirect('login')
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'form': login_form})



@login_required
def profile(request):
    name = request.user.username  # Assuming the username is used for the name
    return render(request, 'profile.html', {'name': name})

def log_out(request):
    messages.success(request, "Logged out successfully")
    logout(request)
    return redirect('home')