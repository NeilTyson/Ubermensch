import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render
import json

from Ubermensch import helper
from orders.forms import OrderForm, ContractForm
from orders.models import Order, OrderLine, InspectorReport, Contract, BillingStatement
from products.models import Product


@login_required
def index(request):

    orders = Order.objects.all()
    return render(request, 'orders/index.html', {'orders': orders})


@login_required
def add_order(request):

    form = OrderForm(request.POST or None)
    orders = Order.objects.all()

    if form.is_valid():
        order = form.save(commit=False)
        order.save()

        messages.success(request, "Pending order placed")
        return render(request, 'orders/index.html', {'orders': orders})

    return render(request, 'orders/add_order.html', {'form': form})


@login_required
def order_details(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        context = {
            'order': order
        }

        return render(request, 'orders/order_detail.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def project_requirements_phase(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        context = {
            'order': order
        }

        return render(request, 'orders/project_requirements.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def purchase_order_phase(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        has_contract = hasattr(order, 'contract')

        context = {
            'order': order,
            'has_contract': has_contract
        }

        return render(request, 'orders/purchase_order_phase.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def product_retrieval_phase(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        context = {
            'order': order
        }

        return render(request, 'orders/product_retrieval.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def delivery(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        context = {
            'order': order
        }

        return render(request, 'orders/delivery.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def installation(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        context = {
            'order': order
        }

        return render(request, 'orders/installation.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def maintenance(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        context = {
            'order': order
        }

        return render(request, 'orders/maintenance.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def inspector_report(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        products = Product.objects.all()

        context = {
            'order': order,
            'products': products
        }

        return render(request, 'orders/inspector_report.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def add_order_line(request):
    order = Order.objects.get(id=request.POST['order'])
    product = Product.objects.get(id=request.POST['product'])
    quantity = request.POST['quantity']
    duration = request.POST['duration']
    manpower = request.POST['manpower']

    OrderLine.objects.create(
        order=order,
        product=product,
        quantity=quantity
    )

    order.has_project_requirements = True
    order.save()

    number = random.randint(1, 999999)
    inspector_no = "I-" + str(number)

    while helper.check_duplicate_numbers(inspector_no, "inspector"):
        number = random.randint(1, 999999)
        inspector_no = "I-" + str(number)

    InspectorReport.objects.create(
        order=order,
        inspector_report_no=inspector_no,
        duration=duration,
        manpower=manpower
    )

    return HttpResponse("added")


@login_required
def view_inspector_report(request, order_id):

    try:
        order = Order.objects.get(id=order_id)
        order_line = OrderLine.objects.filter(order=order_id)
        report_inspector = InspectorReport.objects.get(order=order)

        context = {
            'order': order,
            'order_line': order_line,
            'inspector_report': report_inspector
        }

        return render(request, 'orders/inspector_report_R.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def contract_form(request, order_id):

    try:
        orders = Order.objects.all()
        order = Order.objects.get(id=order_id)
        order_line = OrderLine.objects.filter(order=order)

        form = ContractForm(request.POST or None)

        if form.is_valid():
            contract = form.save(commit=False)
            contract.order = order

            # contract no
            number = random.randint(1, 999999)
            contract_no = "PO-" + str(number)

            while helper.check_duplicate_numbers(contract_no, 'contract'):
                number = random.randint(1, 999999)
                contract_no = "I-" + str(number)

            contract.number = contract_no
            contract.save()

            messages.success(request, "Contract generated!")

            context = {
                'order': order,
                'orders': orders
            }

            return render(request, 'orders/index.html', context)

        context = {
            'order': order,
            'form': form,
            'order_line': order_line,
            'total_price': helper.get_total_price(order),
        }

        return render(request, 'orders/contract_form.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def view_contract(request, order_id):

    try:
        order = Order.objects.get(id=order_id)
        contract = Contract.objects.get(order=order)
        order_line = OrderLine.objects.filter(order=order)
        installation = contract.installation_fee / 100
        engineering = contract.engineering_fee / 100
        consumables = contract.consumables_fee / 100
        sub_total = helper.get_total_price(order)

        context = {
            'order': order,
            'contract': contract,
            'order_line': order_line,
            'sub_total': sub_total,
            'installation': round(installation * sub_total, 2),
            'engineering': round(engineering * sub_total, 2),
            'consumables': round(consumables * sub_total, 2),
            'grand_total': round((installation * sub_total) + (engineering * sub_total) +
                                 (consumables * sub_total) + sub_total, 2)
        }

        return render(request, 'orders/contract.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def generate_billing_statement_1(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        has_contract = hasattr(order, 'contract')
        percentage = 0

        number = random.randint(1, 999999)
        bs_no = "BS-" + str(number)

        while helper.check_duplicate_numbers(bs_no, 'billing'):
            number = random.randint(1, 999999)
            bs_no = "BS-" + str(number)

        if order.contract.payment_terms == "50-40-10":
            percentage = 50
        elif order.contract.payment_terms == "50-30-20":
            percentage = 50

        item = str(percentage) + "% DOWN PAYMENT FOR PROJECT"

        BillingStatement.objects.create(
            order=order,
            number=bs_no,
            percentage=percentage,
            item=item
        )

        context = {
            'order': order,
            'has_contract': has_contract
        }

        messages.success(request, "Billing statement generated!")

        return render(request, 'orders/purchase_order_phase.html', context)

    except Order.DoesNotExist:
        raise Http404('Order does not exist')


@login_required
def view_billing_statement_1(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        billing_statement = BillingStatement.objects.filter(order=order).latest('id')

        context = {
            'order': order,
            'billing_statement': billing_statement,
            'price': round(helper.get_grand_total_price(order) * (billing_statement.percentage / 100), 2)
        }

        return render(request, 'orders/billing_statement.html', context)

    except Order.DoesNotExist:
        raise Http404('Order does not exist')




