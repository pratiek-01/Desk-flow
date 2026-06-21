from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import RequestTicket


class RegisterForm(UserCreationForm):
    """Simple signup form - extends Django's built-in form."""
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RequestTicketForm(forms.ModelForm):
    """Form an employee fills to raise a new asset request."""
    class Meta:
        model = RequestTicket
        fields = ['asset_type', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Why do you need this asset?'}),
        }
