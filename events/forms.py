from django import forms
from django.contrib.auth.models import User
from .models import Event, Attend

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['added_by', ]

        widgets = {
        	'date': forms.DateInput(attrs= { 'type' : 'date' }),
        	'starting_time': forms.TimeInput(attrs= { 'type' : 'time' }),
        	'ending_time': forms.TimeInput(attrs= { 'type' : 'time' }),
        }
    
class SeatForm(forms.ModelForm):
    class Meta:
        model = Attend
        fields = ['seats',]