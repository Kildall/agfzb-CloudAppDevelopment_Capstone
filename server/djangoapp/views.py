from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import LoginForm, RegisterForm
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from requests import post

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
def about(request):
    form = LoginForm()
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', {"login_form": form})


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    form = LoginForm()
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', {"login_form": form})

# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):
    if(request.method == "POST"):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("djangoapp:index")

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    if(request.method == "POST"):
        logout(request)
        return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    register_form = RegisterForm()
    login_form = LoginForm()
    if(request.method == "POST"):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', {"login_form":login_form, "register_form": register_form})
    else:
        return render(request, 'djangoapp/registration.html', {"login_form":login_form, "register_form": register_form})


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    form = LoginForm()
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', {"login_form": form})


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

