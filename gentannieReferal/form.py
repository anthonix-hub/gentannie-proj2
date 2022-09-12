from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import admin
# from phonenumber_field.formfields import PhoneNumberField

from .models import *

class signupForm (UserCreationForm):
    username = forms.CharField(max_length=20, required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    # middle_name = forms.CharField(max_length=20, required=True)
    # Email_address = forms.EmailField(max_length=80, required=True)
    # phone_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            # 'middle_name',
            # 'phone_number',
            )
        widgets = {
            'email': forms.EmailInput(attrs={
                'required':True,
                'placeholder':'@mail.com'
            }),
        }

class referForm(ModelForm):
    class Meta:
        model = user_referal
        fields = ('request_bonus',)