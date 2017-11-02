from django import forms

from core.models import Profile
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
            'involved_people': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)

        involved_people = self.fields['involved_people']
        queryset = Profile.objects.order_by('user_type')
        involved_people.queryset = queryset


