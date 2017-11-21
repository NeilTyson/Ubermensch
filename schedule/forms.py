from django import forms
from django.forms import DateTimeField

from core.models import Profile
from schedule.models import Schedule


class ScheduleForm(forms.ModelForm):

    start_date = DateTimeField(input_formats=["%Y/%m/%d %H:%M"], widget=
                               forms.DateTimeInput(attrs={
                                   'class': 'datetimepicker'
                               }))

    end_date = DateTimeField(input_formats=["%Y/%m/%d %H:%M"], widget=
                             forms.DateTimeInput(attrs={
                                 'class': 'datetimepicker'
                             }))

    class Meta:
        model = Schedule
        fields = ['name', 'description', 'order', 'involved_people', 'start_date', 'end_date']
        widgets = {
            'description': forms.Textarea,
            'involved_people': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)

        involved_people = self.fields['involved_people']
        queryset = Profile.objects.order_by('user_type')
        involved_people.queryset = queryset


class ScheduleEngineerForm(forms.ModelForm):
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
        fields = ['name', 'description', 'involved_people', 'start_date', 'end_date']
        widgets = {
            'description': forms.Textarea,
            'involved_people': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(ScheduleEngineerForm, self).__init__(*args, **kwargs)

        involved_people = self.fields['involved_people']
        queryset = Profile.objects.filter(user_type="Engineer")
        involved_people.queryset = queryset

