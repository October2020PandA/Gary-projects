from django.db import models
from django import forms
from django.forms import ModelForm
from users.models import *
from .models import *
import datetime


class Ride(models.Model):
    date = models.DateField()
    departure = models.CharField(max_length=350)
    destination = models.CharField(max_length=350)
    time = models.TimeField()
    created_by = models.ForeignKey(
        User, related_name="created_ride", on_delete=models.CASCADE, null=True)
    joined_by = models.ManyToManyField(User, related_name="joined_rides")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RideForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['date', 'departure', 'destination', 'time']
        widgets = {
            'date': forms.DateInput(format=('%d-%m-%Y'), attrs={'firstDay': 1, 'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'pl', 'format': 'yyyy-mm-dd', 'type': 'date'}),
        }
