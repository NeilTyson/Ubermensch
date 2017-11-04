from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render

from orders.forms import OrderForm, AccreditationForm
from orders.models import Order


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
def accreditation_phase(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        context = {
            'order': order
        }

        return render(request, 'orders/accreditation.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


@login_required
def upload_documents(request, order_id):

    form = AccreditationForm(request.POST or None)
    order = Order.objects.get(id=order_id)

    if form.is_valid():
        order_accreditation = form.save(commit=False)
        order_accreditation.save()

        context = {
            'order': order
        }

        messages.success(request, "Documents uploaded successfully!")
        return render(request, 'orders/accreditation.html', context)

    context = {
        'form': form,
        'order': order
    }

    return render(request, 'orders/upload-accreditation.html', context)



