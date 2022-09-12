from django import forms
from django.db.models import fields
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import admin
from phonenumber_field.formfields import PhoneNumberField

from django.core.exceptions import ValidationError

from .models import *

def file_size(value): # add this to some file where you can import it from
    # limit = 2 * 1024 
    limit = 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MiB.')

class signupForm (UserCreationForm):
    username = forms.CharField(max_length=20, required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            )
        
    def save(self, commit = True):
        user = super(signupForm,self).save()
        self.middle_name = self.cleaned_data['middle_name']
        if commit:
            user.save()
            return user

class Supreme_plus_Unlocked_form(ModelForm):
    payment_proof = forms.FileField(validators=[file_size])
    class Meta:
        model = Supreme_plus_UnLocked
        fields = ('plan_name', 'payment_proof')

class Supreme_plus_Locked_form(ModelForm):
    payment_proof = forms.FileField(validators=[file_size])
    class Meta:
        model = Supreme_plus_Locked
        fields = ('plan_name', 'payment_proof')

class Supreme_plus_Savings_form(ModelForm):
    payment_proof = forms.FileField(validators=[file_size])
    class Meta:
        model = Supreme_plus_Savings
        fields = ('plan_name', 'payment_proof')

class users_detailsForm(ModelForm):

    class Meta:
        model = users_details
        fields = (
            'account_number', 'account_name',
            'bank_name', 'phone_number',
            'profile_pic',
             )

class withdraw_requestForm(ModelForm):
    class Meta:
        model = withdrawal_table
        fields = ('amount',)


class Supreme_plus_Unlocked_withdrawalForm(ModelForm):
    class Meta:
        model = withdrawal_tabel
        fields = ('request',)

class Supreme_plus_Locked_withdrawalForm(ModelForm):
    class Meta:
        model = Supreme_plus_Locked
        fields = ('request',)

class Supreme_plus_Savings_withdrawalForm(ModelForm):
    class Meta:
        model = Supreme_plus_Savings
        fields = ('request',)

class Supreme_plus_Unlocked_pay_comfirmForm(ModelForm):
    class Meta:
        model = Supreme_plus_Unlocked_payment_comfirm
        fields = ('request',)

class Supreme_plus_Locked_pay_comfirmForm(ModelForm):
    class Meta:
        model = Supreme_plus_Locked_payment_comfirm
        fields = ('request',)

class Supreme_plus_Savings_pay_comfirmForm(ModelForm):
    class Meta:
        model = Supreme_plus_Savings_payment_comfirm
        fields = ('request',)
        
