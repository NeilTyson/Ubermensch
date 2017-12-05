from django.forms import ModelForm, widgets, DateTimeField
from django import forms

from core.models import Profile
from maintenance.models import MaintenanceContract, TroubleTicket
from orders.models import BillingStatement
from schedule.models import Schedule


class MaintenanceContractForm(ModelForm):

    class Meta:
        model = MaintenanceContract
        fields = '__all__'
        exclude = ['number', 'order', 'generated_by', 'is_current', 'date_generated']

        widgets = {
            'duration': forms.widgets.TextInput(attrs={
                'placeholder': 'In years'
            })
        }


class ScheduleMaintenanceForm(ModelForm):

    class Meta:
        model = Schedule
        fields = '__all__'
        exclude = ['is_completed', 'order']
        widgets = {
            'description': forms.widgets.Textarea(attrs={
                'class': 'form-control'
            }),
            'involved_people': forms.widgets.CheckboxSelectMultiple()
        }

    name = forms.CharField(disabled=True)
    start_date = forms.DateTimeField(disabled=True, input_formats=["%B %d, %Y %I:%M %p"],)
    end_date = forms.DateTimeField(disabled=True, input_formats=["%B %d, %Y %I:%M %p"],)

    def __init__(self, *args, **kwargs):
        super(ScheduleMaintenanceForm, self).__init__(*args, **kwargs)

        involved_people = self.fields['involved_people']
        queryset = Profile.objects.filter(user_type="Engineer")
        involved_people.queryset = queryset


class TroubleTicketForm(ModelForm):

    class Meta:
        model = TroubleTicket
        fields = "__all__"
        exclude = ['order', 'date_created', 'status', 'generated_by', 'has_official_receipt', 'has_billing_statement']
        widgets = {
            'subject': forms.widgets.TextInput()
        }


class ScheduleTroubleForm(forms.ModelForm):
    start_date = DateTimeField(input_formats=["%Y/%m/%d %H:%M"], widget=
    forms.DateTimeInput(attrs={
        'class': 'datetimepicker'
    }))

    end_date = DateTimeField(input_formats=["%Y/%m/%d %H:%M"], widget=
    forms.DateTimeInput(attrs={
        'class': 'datetimepicker'
    }))

    name = forms.CharField(disabled=True)

    class Meta:
        model = Schedule
        fields = '__all__'
        exclude = ('is_completed', 'order')
        widgets = {
            'description': forms.Textarea(),
            'involved_people': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(ScheduleTroubleForm, self).__init__(*args, **kwargs)

        involved_people = self.fields['involved_people']
        queryset = Profile.objects.filter(user_type="Engineer")
        involved_people.queryset = queryset


class TroubleBillingStatementForm(ModelForm):

    class Meta:
        model = BillingStatement
        fields = ['item', 'price']