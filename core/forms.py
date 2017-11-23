from django import forms
from django.forms.models import ModelForm

from core.models import Profile, Customer


class UserForm(ModelForm):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'password', 'confirm_password', 'user_type', 'address', 'email']


class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'



