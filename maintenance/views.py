import random
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from Ubermensch import helper
from core.models import Profile
from maintenance.forms import MaintenanceContractForm
from maintenance.models import MaintenanceContract
from orders.models import Order

@login_required
def maintenance_overview(request, order_id):

    try:
        order = Order.objects.get(id=order_id)
        context = {
            'order': order
        }

        return render(request, 'maintenance/maintenance.html', context)

    except Order.DoesNotExist:
        raise Http404('Order Does Not Exist')


@login_required
def maintenance_contract_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        expiration_date = order.contract.warranty_expiration_date
        contracts = MaintenanceContract.objects.all()

        context = {
            'order': order,
            'expiration_date': expiration_date,
            'is_warranty_period': expiration_date > datetime.now().date(),
            'contracts': contracts
        }

        return render(request, 'maintenance/maintenance_contract_overview.html', context)

    except Order.DoesNotExist:
        raise Http404('Order Does Not Exist')


@login_required
def add_maintenance_contract(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        form = MaintenanceContractForm(request.POST or None)

        context = {
            'form': form
        }

        if form.is_valid():
            contract = form.save(commit=False)
            contract.order = order

            number = random.randint(1, 999999)
            mc_no = "MC-" + str(number)

            while helper.check_duplicate_numbers(mc_no, 'maintenance'):
                number = random.randint(1, 999999)
                mc_no = "MC-" + str(number)

            profile = Profile.objects.get(user=request.user)
            contract.number = mc_no
            contract.generated_by = profile
            contract.save()

            messages.success(request, 'Maintenance contract added!')
            return redirect('maintenance:overview', order_id=order.id)

        return render(request, 'maintenance/maintenance_form.html', context)
    except Order.DoesNotExist:
        raise Http404('Order does not exist')