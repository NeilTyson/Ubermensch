from django.forms import ModelForm, widgets
from django import forms

from maintenance.models import MaintenanceContract


class MaintenanceContractForm(ModelForm):

    class Meta:
        model = MaintenanceContract
        fields = '__all__'
        exclude = ['number', 'order', 'generated_by', 'is_current']

        widgets = {
            'duration': forms.widgets.TextInput(attrs={
                'placeholder': 'In years'
            })
        }
