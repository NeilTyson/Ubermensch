from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.views import View, generic
from django.views.generic import CreateView

from core.forms import UserForm, CustomerForm
from core.models import Profile, Customer


# def index(request):
#     return HttpResponse("Hello world")

class IndexView(LoginRequiredMixin, generic.ListView):

    template_name = 'core/index.html'
    context_object_name = "profiles"

    def get_queryset(self):
        return Profile.objects.all()


# class ProfileFormView(View):
#
#     form_class = UserForm
#     template_name = 'templates/core/profile_form.html'
#
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
#
#             user = form.save(commit=False)
#
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             # user.set_password(password)
#             # user.save()
#
#             existing = User.objects.filter(username=username)
#
#             if existing:
#                 return render(request, self.template_name, {'error': 'Username already exists'})
#
#             user = User.objects.create_user(username, None, password)
#
#             Profile.objects.create(user=user, first_name=request.POST['first_name'],
#                                    last_name=request.POST['last_name'],
#                                    user_type=request.POST['user_type'],
#                                    address=request.POST["address"])
#
#         return redirect('core:index')


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

        return render(request, 'core/home.html', {'user': user_profile})


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

        messages.success(request, "Customer added successfully!")
        return render(request, 'core/customer_index.html', {'customers': customers})

    context = {'form': form}
    return render(request, 'core/add_customer.html', context)



