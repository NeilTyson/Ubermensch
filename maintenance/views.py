import random
from datetime import datetime

import decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from Ubermensch import helper
from core.models import Profile
from maintenance.forms import MaintenanceContractForm, ScheduleMaintenanceForm
from maintenance.models import MaintenanceContract
from orders.models import Order, BillingStatement, OfficialReceipt
from schedule.models import Schedule


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
        contracts = MaintenanceContract.objects.filter(order=order)
        maintenance_expiration_date = ''
        expiration_date = order.contract.warranty_expiration_date

        if MaintenanceContract.objects.filter(order=order).count() == 0:
            current_contract = None
        else:
            current_contract = MaintenanceContract.objects.filter(order=order, is_current=True)[0]

        if current_contract is not None:
            maintenance_expiration_date = helper.add_years(
                current_contract.date_generated,
                current_contract.duration
            )

            schedules = Schedule.objects.filter(order=order).filter(name__contains='Maintenance')
            maintenance_dates = []
            for s in schedules:
                maintenance_dates.append(s.start_date.date().strftime('%B %d, %Y'))

            b_statements = BillingStatement.objects.filter(order=order).filter(item__contains='Maintenance')
            bs_list = []
            for bs in b_statements:
                bs_list.append(bs.date_created.date().strftime('%B %d, %Y'))

            context = {
                'order': order,
                'expiration_date': expiration_date,
                'is_warranty_period': expiration_date > datetime.now().date(),
                'contracts': contracts,
                'current_contract': current_contract,
                'maintenance_expiration_date': maintenance_expiration_date,
                'date_intervals': helper.get_date_intervals(
                    current_contract.date_generated,
                    maintenance_expiration_date,
                    # terms of payment
                    current_contract.payment
                ),
                'schedules': maintenance_dates,
                'billing_statements': bs_list
            }

        else:
            context = {
                'order': order,
                'expiration_date': expiration_date,
                'is_warranty_period': expiration_date > datetime.now().date(),
                'contracts': contracts,
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
            contract.is_current = True
            contract.save()

            messages.success(request, 'Maintenance contract added!')
            return redirect('maintenance:overview', order_id=order.id)

        return render(request, 'maintenance/maintenance_form.html', context)
    except Order.DoesNotExist:
        raise Http404('Order does not exist')


@login_required
def generate_billing_statement(request):
    maintenance_id = request.POST['id']
    order_id = request.POST['order']
    order = Order.objects.get(id=order_id)
    maintenance_contract = MaintenanceContract.objects.get(id=maintenance_id)
    profile = Profile.objects.get(user=request.user)
    maintenance_expiration_date = helper.add_years(
                maintenance_contract.date_generated,
                maintenance_contract.duration
            )

    number = random.randint(1, 999999)
    bs_no = "BS-" + str(number)

    while helper.check_duplicate_numbers(bs_no, 'billing'):
        number = random.randint(1, 999999)
        bs_no = "BS-" + str(number)

    percentage = 100 / len(helper.get_date_intervals(maintenance_contract.date_generated, maintenance_expiration_date,
                              maintenance_contract.payment))

    item = str(percentage) + '% DOWN PAYMENT FOR MAINTENANCE SERVICE'

    BillingStatement.objects.create(
        order=order,
        number=bs_no,
        item=item,
        percentage=percentage,
        generated_by=profile,
        price=maintenance_contract.price/decimal.Decimal(percentage),
        state=2
    )

    messages.success(request, 'Billing Statement Generated')
    return redirect('maintenance:contract-view', order_id=order.id)


@login_required
def schedule_maintenance(request):
    date = request.GET['date']
    order_id = request.GET['order']
    order = Order.objects.get(id=order_id)

    form = ScheduleMaintenanceForm(request.POST or None, initial={
        'name': 'Conduct Maintenance for ' + order.customer.company_name,
        'start_date': date + ' 8:30 am',
        'end_date': date + ' 5:30 pm'
    })

    if form.is_valid():
        schedule = form.save(commit=False)
        schedule.order = order
        engineers = request.POST.getlist('involved_people')
        schedule.save()

        s = Schedule.objects.latest('id')

        if helper.check_overlaps(engineers, s.start_date, s.end_date):
            context = {
                'form': form,
                'error': "Failed to add schedule. Overlap/s or conflict/s found"
            }

            return render(request, 'schedule/create_schedule.html', context)

        for e in engineers:
            schedule.involved_people.add(e)

        messages.success(request, 'Schedule added!')
        return redirect('maintenance:overview', order_id=order.id)

    context = {
        'form': form
    }

    return render(request, 'maintenance/schedule_maintenance.html', context)


@login_required
def generate_official_receipt(request):
    maintenance_id = request.POST['id']
    order_id = request.POST['order']
    order = Order.objects.get(id=order_id)
    maintenance_contract = MaintenanceContract.objects.get(id=maintenance_id)
    profile = Profile.objects.get(user=request.user)
    maintenance_expiration_date = helper.add_years(
                maintenance_contract.date_generated,
                maintenance_contract.duration
            )

    number = random.randint(1, 999999)
    or_no = "OR-" + str(number)

    while helper.check_duplicate_numbers(or_no, 'official'):
        number = random.randint(1, 999999)
        pr_no = "OR-" + str(number)

    percentage = len(helper.get_date_intervals(maintenance_contract.date_generated, maintenance_expiration_date,
                              maintenance_contract.payment))

    item = str(percentage) + '% DOWN PAYMENT FOR MAINTENANCE SERVICE'

    OfficialReceipt.objects.create(
        order=order,
        number=or_no,
        percentage=percentage,
        generated_by=profile,
        state=2
    )

    official = OfficialReceipt.objects.latest('id')

    schedule = Schedule.objects.filter(order=order).filter(name__contains='Maintenance',
                                                           start_date__month=official.date_created.month)[0]
    schedule.is_completed = True
    schedule.save()

    messages.success(request, 'Official Receipt Generated')
    return redirect('maintenance:contract-view', order_id=order.id)
