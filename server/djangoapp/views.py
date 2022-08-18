from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .restapis import get_dealers_from_cf, get_dealers_by_param, get_dealer_review_from_cf, post_review
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
def get_dealerships(request, state=None):
    form = LoginForm()
    if request.method == "GET":
        url = 'https://2265855a.us-east.apigw.appdomain.cloud/final/get_dealership'
        if not state:
            dealerships = get_dealers_from_cf(url)
        else:
            dealerships = get_dealers_by_param(url, state=state)
        return render(request, 'djangoapp/index.html', {"login_form": form, "dealerships": dealerships})


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    form = LoginForm()
    if request.method == "GET":
        dealer_url = 'https://2265855a.us-east.apigw.appdomain.cloud/final/get_dealership'
        reviews_url = 'https://2265855a.us-east.apigw.appdomain.cloud/final/get_review'
        reviews = get_dealer_review_from_cf(reviews_url, id=id)
        dealership = get_dealers_by_param(dealer_url, id=id)
        if(dealership):
            dealership = dealership[0]
        if(request.user.is_authenticated):
            return render(request, 'djangoapp/dealer_details.html', {"login_form": form, "reviews": reviews, "dealership": dealership,
             "show_review_form": True, "review_form": ReviewForm(name=request.user.first_name + " " + request.user.last_name)})
        else:
            return render(request, 'djangoapp/dealer_details.html', {"login_form": form, "reviews": reviews, "dealership": dealership})


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    if(request.method == "POST"):
        form = ReviewForm(request.POST, name=request.user.first_name + " " + request.user.last_name)
        post_review_url = 'https://2265855a.us-east.apigw.appdomain.cloud/final/submit_review'
        print(form.is_valid())
        for field in form:
            print("Error: ", field.name, field.value())
        if form.is_valid():
            car_model = CarModel.objects.get(id=form.cleaned_data["selected_car"])
            car_make = car_model.make.name
            car_year = str(car_model.year.year)
            review = DealerReview(dealership=dealer_id, purchase=form.cleaned_data["purchase"], name=form.cleaned_data["name"], review=form.cleaned_data["review"],
                    purchase_date=form.cleaned_data["purchase_date"], car_make=car_make, car_model=car_model, car_year=car_year)
            post_review(post_review_url, review=review)
            return redirect("djangoapp:details", id=dealer_id)
        else:
            return redirect("djangoapp:details", id=dealer_id)
