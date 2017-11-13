import json
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render

from Ubermensch import helper
from core.models import Profile
from schedule.forms import ScheduleForm
from schedule.models import Schedule


@login_required
def index(request):

    schedules = Schedule.objects.order_by('deadline_date')
    context = {'schedules': schedules}

    return render(request, 'schedule/index.html', context)


@login_required
def details(request, pk):
    try:
        schedule = Schedule.objects.get(id=pk)

        context = {
            'schedule': schedule
        }

        # return render(request, 'orders/order_detail.html', context)
        return HttpResponse("This is schedule %s" % pk)

    except Schedule.DoesNotExist:
        raise Http404("Schedule does not exist")


@login_required
def create_schedule(request):
    form = ScheduleForm(request.POST or None)
    schedules = Schedule.objects.order_by('deadline_date')

    if form.is_valid():
        schedule = form.save(commit=False)

        people = request.POST.getlist('involved_people')

        start_date = datetime.strptime(request.POST['start_date'], '%Y/%m/%d %H:%M')
        end_date = datetime.strptime(request.POST['end_date'], '%Y/%m/%d %H:%M')

        if end_date < start_date:

            context = {
                'form': form,
                'error': "End date cannot be before the start date"
            }

            return render(request, 'schedule/create_schedule.html', context)

        if start_date < datetime.now() or end_date < datetime.now():
            context = {
                'form': form,
                'error': "Start dates and end dates cannot be past the current date"
            }

            return render(request, 'schedule/create_schedule.html', context)

        if helper.check_overlaps(people, start_date, end_date):

            context = {
                'form': form,
                'error': "Failed to add schedule. Overlap/s or conflict/s found"
            }

            return render(request, 'schedule/create_schedule.html', context)

        else:
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
    query = Schedule.objects.get(pk=schedule).involved_people.all()

    serialized = serializers.serialize('json', query)

    data = {'data': serialized}

    return JsonResponse(data)


# ajax of displaying the schedules on the calendar
def display_events(request):
    schedules = Schedule.objects.all()

    serialized = serializers.serialize('json', schedules)
    data = {'schedules': serialized}

    return JsonResponse(data)



