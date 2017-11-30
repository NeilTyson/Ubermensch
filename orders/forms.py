from django.forms import ModelForm
from django import forms
from orders.models import Order, Contract, ProgressReport
from schedule.models import Schedule


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ['customer']


class ContractForm(ModelForm):

    class Meta:
        model = Contract
        fields = ['installation_fee', 'engineering_fee', 'consumables_fee', 'payment_terms',
                  'delivery_terms', 'completion', 'warranty']
        widgets = {
            'installation_fee': forms.NumberInput(attrs={'placeholder': "In percentage"}),
            'engineering_fee': forms.NumberInput(attrs={'placeholder': "In percentage"}),
            'consumables_fee': forms.NumberInput(attrs={'placeholder': "In percentage"}),
            'completion': forms.NumberInput(attrs={'placeholder': "In weeks"}),
            'warranty': forms.NumberInput(attrs={'placeholder': "In years"}),
        }


class ProgressReportForm(ModelForm):

    class Meta:
        model = ProgressReport
        fields = ['title', 'report_progress']
        widgets = {
            'report_progress': forms.Textarea(attrs={'class': 'form-control'})
        }


class ExtendProjectForm(ModelForm):

    class Meta:
        model = Schedule
        fields = ['end_date']
