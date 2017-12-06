from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View, generic
from Ubermensch import helper
from core.forms import UserForm, CustomerForm
from core.models import Profile, Customer
from orders.forms import OrderForm
from schedule.models import Schedule


class IndexView(LoginRequiredMixin, generic.ListView):

    template_name = 'core/index.html'
    context_object_name = "profiles"

    def get_queryset(self):
        return Profile.objects.all()


def add_user(request):

    form = UserForm(request.POST or None)

    if form.is_valid():

        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['confirm_password']

        if helper.is_unique(username):

            User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)

            user = User.objects.get(username=username)

            if cpassword != password:
                return HttpResponse("passwords do not match")

            Profile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=request.POST['address'],
                user_type=request.POST['user_type']
            )

            return redirect('core:index')

        else:

            return HttpResponse('username is taken')

    context = {'form': form}
    return render(request, 'core/add_user.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

        return redirect('core:login')


class SignInView(View):
    template_name = 'core/login.html'

    def get(self, request):

        if request.user.is_authenticated:
            return redirect('core:index')
        return render(request, self.template_name, None)

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:

            login(request, user)

            return redirect('core:index')

        else:
            return render(request, self.template_name, {'error': 'Invalid login credentials'})


@login_required
def home(request):

    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)

        if user_profile.user_type != 'ADMIN':
            return redirect('core:home-dashboard')


@login_required
def home_dashboard(request):

    my_schedules = Schedule.objects.filter(involved_people__user=request.user)

    context = {
        'my_schedules': my_schedules
    }

    return render(request, 'dashboards/dashboard.html', context)


@login_required
def customer_index(request):

    customers = Customer.objects.all()

    return render(request, 'core/customer_index.html', {'customers': customers})


@login_required
def add_customer(request):

    form = CustomerForm(request.POST or None)
    customers = Customer.objects.all()

    if form.is_valid():
        customer = form.save(commit=False)
        customer.save()

        context = {
            'form': OrderForm()
        }

        messages.success(request, "Customer added successfully!")
        return redirect('orders:add_order')

    context = {'form': form}
    return render(request, 'core/add_customer.html', context)


@login_required
def users_index(request):

    profiles = Profile.objects.all()

    context = {
        'profiles': profiles
    }

    return render(request, 'core/users.html', context)


# ajax
def get_current_datetime(request):

    today = datetime.now().strftime('%B %d, %Y %I:%M %p')
    return JsonResponse(today, safe=False)



