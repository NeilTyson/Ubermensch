from django import forms

from schedule.models import Schedule


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = ['name', 'description', 'customer', 'involved_people', 'deadline_date',]
        widgets = {
            'deadline_date': forms.DateInput(attrs={
                'class': 'datepicker'
            }),

            'description': forms.Textarea,
        }
