import random
import math
import decimal
from datetime import datetime

import inflect as inflect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

from Ubermensch import helper
from core.models import Profile
from orders.forms import OrderForm, ContractForm
from orders.models import Order, OrderLine, InspectorReport, Contract, BillingStatement, OfficialReceipt, \
    DeliveryReceipt
from products.models import Product
from schedule.forms import ScheduleForm, ScheduleEngineerForm, ScheduleDeliveryForm
from schedule.models import Schedule


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

        messages.success(request, "Order placed")
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
    profile = Profile.objects.get(user=request.user)

    while helper.check_duplicate_numbers(inspector_no, "inspector"):
        number = random.randint(1, 999999)
        inspector_no = "I-" + str(number)

    InspectorReport.objects.create(
        order=order,
        inspector_report_no=inspector_no,
        duration=duration,
        manpower=manpower,
        generated_by=profile
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

    profile = Profile.objects.get(user=request.user)

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

            order.has_contract = True
            order.save()

            # TODO revise continue
            if contract.payment_terms == "50-40-10":
                term = contract.payment_terms.split("-")
                contract.first_percentage = term[0]
                contract.second_percentage = term[1]
                contract.third_percentage = term[2]

            elif contract.payment_terms == "50-30-20":
                term = contract.payment_terms.split("-")
                contract.first_percentage = term[0]
                contract.second_percentage = term[1]
                contract.third_percentage = term[2]

            elif contract.payment_terms == "Full Payment":
                pass


            contract.number = contract_no
            contract.generated_by = profile
            contract.save()

            messages.success(request, "Contract generated!")

            context = {
                'order': order,
                'orders': orders,
                'has_contract': hasattr(order, "contract")
            }

            return render(request, 'orders/purchase_order_phase.html', context)

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
def generate_billing_statement(request, order_id, percentage, code, template_no):
    try:
        order = Order.objects.get(id=order_id)

        number = random.randint(1, 999999)
        bs_no = "BS-" + str(number)

        while helper.check_duplicate_numbers(bs_no, 'billing'):
            number = random.randint(1, 999999)
            bs_no = "BS-" + str(number)

        item = helper.get_item_description(code, order.id)
        user = Profile.objects.get(user=request.user)

        BillingStatement.objects.create(
            order=order,
            number=bs_no,
            item=item,
            percentage=int(percentage),
            generated_by=user
        )

        context = {
            'order': order
        }

        messages.success(request, "Billing statement generated!")
        template = helper.get_payment_template(template_no)

        return render(request, template, context)

    except Order.DoesNotExist:
        raise Http404('Order does not exist')


@login_required
def billing_statement_lists(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        context = {
            'order': order,
            'billing_statements': order.billingstatement_set.order_by("-date_created")
        }

        return render(request, "orders/billing_statement_list.html", context)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def view_billing_statement(request, id):
    try:
        billing_statement = BillingStatement.objects.get(id=id)
        order = Order.objects.filter(billingstatement=billing_statement)[0]

        context = {
            "billing_statement": billing_statement,
            "order": order,
            "price": round(helper.get_grand_total_price(order) * (billing_statement.percentage/ 100), 2)
        }

        return render(request, "orders/billing_statement.html", context)
    except BillingStatement.DoesNotExist:
        raise Http404("Billing statement does not exist")


@login_required
def generate_official_receipt(request, order_id, percentage, template_no):
    try:
        order = Order.objects.get(id=order_id)

        number = random.randint(1, 999999)
        or_no = "OR-" + str(number)

        while helper.check_duplicate_numbers(or_no, 'official'):
            number = random.randint(1, 999999)
            or_no = "OR-" + str(number)

        user = Profile.objects.get(user=request.user)

        OfficialReceipt.objects.create(
            order=order,
            number=or_no,
            percentage=int(percentage),
            generated_by=user
        )

        context = {
            'order': order
        }

        messages.success(request, "Official receipt generated!")
        template = helper.get_payment_template(template_no)

        # if delivery
        if template_no == "2":
            order.is_delivered = True
            order.status = "Installation"
            order.save()

        return render(request, template, context)

    except Order.DoesNotExist:
        raise Http404('Order does not exist')


@login_required
def official_receipt_list(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        context = {
            'order': order,
            'official_receipts': order.officialreceipt_set.order_by("-date_created")
        }

        return render(request, "orders/official_receipt_list.html", context)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")

@login_required
def view_official_receipt(request, id):

    try:
        official_receipt = OfficialReceipt.objects.get(id=id)
        order = Order.objects.filter(officialreceipt=official_receipt)[0]
        percentage = official_receipt.percentage
        total = percentage / 100 * helper.get_grand_total_price(order)
        vat = total * decimal.Decimal(0.12)

        fraction, whole = math.modf(round(total, 2))
        fraction = fraction * 100

        i = inflect.engine()
        whole_number = i.number_to_words(int(whole))
        decimal_part = i.number_to_words(int(fraction))

        context = {
            'amount': round(total, 2),
            'order': order,
            'official_receipt': official_receipt,
            'vat': round(vat, 2),
            'total': round(total - vat, 2),
            'pesos': whole_number,
            'centavos': decimal_part
        }

        return render(request, 'orders/official_receipt.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def schedule_engineers(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        has_contract = hasattr(order, 'contract')

        form = ScheduleEngineerForm(request.POST or None, initial={
            'name': "Installation for " + str(order.customer),
        })
        engineers = request.POST.getlist('involved_people')

        if form.is_valid():
            schedule = form.save(commit=False)

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

            if helper.check_overlaps(engineers, start_date, end_date):

                context = {
                    'form': form,
                    'error': "Failed to add schedule. Overlap/s or conflict/s found"
                }

                return render(request, 'schedule/create_schedule.html', context)

            else:
                order.has_scheduled_engineers = True
                order.has_contract_done = True
                order.status = "Product Retrieval"
                order.save()
                schedule.order = order
                schedule.save()

                for p in engineers:
                    schedule.involved_people.add(p)

                messages.success(request, "Schedule added successfully!")

                context = {
                    'order': order,
                    'has_contract': has_contract
                }

                return render(request, 'orders/purchase_order_phase.html', context)

        context = {'form': form}

        return render(request, 'schedule/create_schedule.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def schedule_delivery(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        form = ScheduleDeliveryForm(request.POST or None, initial={
            'name': "Delivery for " + str(order.customer),
        })
        people = request.POST.getlist('involved_people')

        if form.is_valid():
            schedule = form.save(commit=False)

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
                order.has_scheduled_delivery = True
                order.save()
                schedule.order = order
                schedule.save()

                for p in people:
                    schedule.involved_people.add(p)

                messages.success(request, "Schedule added successfully!")

                context = {
                    'order': order,
                }

                return render(request, 'orders/delivery.html', context)

        context = {'form': form}

        return render(request, 'schedule/create_schedule.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def generate_delivery_receipt(request, order_id, template_no):
    try:
        order = Order.objects.get(id=order_id)
        user = Profile.objects.get(user=request.user)

        number = random.randint(1, 999999)
        dr_no = "DR-" + str(number)

        while helper.check_duplicate_numbers(dr_no, 'deliver'):
            number = random.randint(1, 999999)
            dr_no = "DR-" + str(number)

        DeliveryReceipt.objects.create(
            order=order,
            number=dr_no,
            generated_by=user
        )

        context = {
            'order': order
        }
        template = helper.get_payment_template(template_no)
        messages.success(request, "Delivery Receipt generated!")

        return render(request, template, context)


    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def delivery_receipt_list(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        context = {
            'order': order,
            'delivery_receipts': order.deliveryreceipt_set.order_by("-date_created")
        }

        return render(request, "orders/delivery_receipt_list.html", context)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def view_delivery_receipt(request, id):
    try:
        delivery_receipt = DeliveryReceipt.objects.get(id=id)
        order = Order.objects.filter(deliveryreceipt=delivery_receipt)[0]
        order_line = OrderLine.objects.filter(order=order)

        context = {
            'order': order,
            'delivery_receipt': delivery_receipt,
            'order_line': order_line
        }

        return render(request, "orders/delivery_receipt.html", context)

    except DeliveryReceipt.DoesNotExist:
        raise Http404('Delivery Receipt does not exist')


@login_required
def view_project(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        context = {
            'order': order
        }

        return render(request, 'orders/project.html', context)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")


# ajax
def view_engineers(request):

    order_id = request.POST['order']
    order = Order.objects.get(id=order_id)
    schedule = Schedule.objects.filter(
        involved_people__user_type="Engineer",
        order=order
    )

    engineers = schedule[0].involved_people.all()

    serialize = serializers.serialize('json', engineers)

    return JsonResponse(serialize, safe=False)


# ajax
def view_delivery_people(request):

    order_id = request.POST['order']
    order = Order.objects.get(id=order_id)
    schedule = Schedule.objects.filter(
        involved_people__user_type="Inventory",
        order=order
    )

    people = schedule[0].involved_people.all()

    serialize = serializers.serialize('json', people)

    return JsonResponse(serialize, safe=False)


