from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from core.models import Profile
from schedule.forms import ScheduleForm
from schedule.models import Schedule


@login_required
def index(request):

    schedules = Schedule.objects.all()
    context = {'schedules': schedules}

    return render(request, 'schedule/index.html', context)


@login_required
def create_schedule(request):
    form = ScheduleForm(request.POST or None)
    schedules = Schedule.objects.all().order_by('deadline_date')

    if form.is_valid():
        schedule = form.save(commit=False)
        deadline_time = request.POST['deadline_time']
        people = request.POST.getlist('involved_people')

        if not deadline_time.lstrip():
            return render(request, 'schedule/create_schedule.html',
                          {'error': 'Please input a valid time',
                           'form': form})

        deadline_time_f = datetime.strptime(deadline_time, "%H:%M").time()

        schedule.deadline_time = deadline_time_f
        schedule.save()

        for p in people:
            schedule.involved_people.add(p)

        messages.success(request, "Schedule added successfully!")
        return render(request, 'schedule/index.html', {'schedules': schedules})

    context = {'form': form}

    return render(request, 'schedule/create_schedule.html', context)


# ajax
def display_user_type(request):
    user = Profile.objects.get(user=request.user)

    data = {
        'user_type': user.user_type
    }

    return JsonResponse(data)


# ajax of viewing involved people
def view_involved_people(request):
    schedule = request.POST['schedule']
    query = Schedule.objects.get(pk=schedule)

    x = serializers.serialize('json', query)

    data = {'people': x}

    return JsonResponse(data)



