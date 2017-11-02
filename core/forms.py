from django import forms
from django.forms.models import ModelForm

from core.models import Profile, Customer


class UserForm(ModelForm):
    username = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'password', 'user_type', 'address')


class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = ['company_name', 'contact_first_name', 'contact_last_name', 'email_address', 'contact_no', 'address']



