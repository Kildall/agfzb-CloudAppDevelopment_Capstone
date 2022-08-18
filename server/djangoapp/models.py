from cProfile import label
from tkinter import Widget
from django.db import models
from django.utils.timezone import now
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import json

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), max_length=50)

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name"]

class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CarModel(models.Model):

    class VehicleTypes(models.TextChoices):
        SUV = 'SUV'
        ATV = 'ATV'
        Sedan = 'Sedan'
        Wagon = 'Wagon'
        Compact = 'Compact'
    
    make = models.ForeignKey(to=CarMake, on_delete=models.DO_NOTHING)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=50)
    type = models.CharField(choices=VehicleTypes.choices, max_length=100)
    year = models.DateField()

    def __str__(self):
        return self.name

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data

class DealerReview:
    def __init__(self, dealership, purchase, name, review, purchase_date, car_make, car_model, car_year):
        from .restapis import analyze_review_sentiments
        self.dealership = dealership
        self.purchase = purchase
        self.name = name
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = analyze_review_sentiments(review)

class ReviewForm(forms.Form):
    CHOICES= [(car.id, car.make.name +" - "+ car.name +" - "+ str(car.year.year)) for car in CarModel.objects.all()]
    name = forms.CharField(label="Name", max_length=50, disabled=True)
    selected_car = forms.ChoiceField(choices=CHOICES, initial=-1, required=False)
    purchase = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id':'chkPurchase'}), initial=False)
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    review = forms.CharField(label="Review", max_length=500, widget=forms.Textarea(attrs={'style': 'resize: none;'}))

    def __init__(self,*args, name="",**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["name"].initial = name

    
    