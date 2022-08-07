from django.db import models
from django.utils.timezone import now
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import admin

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









# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data