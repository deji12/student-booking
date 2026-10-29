from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_username_existence(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError('This username is already in use')
    
def validate_email_existence(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('This email is already in use')

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, validators=[validate_username_existence])
    email = forms.EmailField(validators=[validate_email_existence])
    password = forms.CharField(widget=forms.PasswordInput())
    
