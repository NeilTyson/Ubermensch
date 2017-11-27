from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from inventory.models import Product, Supplier, Category, Order, OrderLine


@login_required
def index(request):

    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'inventory/index.html', context)


def order_details_inventory(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        orderline = OrderLine.objects.filter(order=order)

        context = {
            'order': order,
            'orderlines': orderline,
        }

        return render(request, 'inventory/order_detail_inventory.html', context)

    except Order.DoesNotExist:
        raise Http404("Order does not exist")


def inventory_order(request):
    orders = Order.objects.all()
    return render(request, 'inventory/inventory_order.html', {'orders': orders})


def request_inventory(request):
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/request_inventory.html', {'products': products, 'suppliers': suppliers})


#TODO need palitan below cuz ajax gamit
def get_products_using_supplier(request, supplier_name):
    try:
        supplier = Supplier.objects.get(name=supplier_name)
        products = Product.objects.filter(supplier=supplier)
        return render(request, '', {'products':products})

    except Product.DoesNotExist:
        raise Http404("Invalid Supplier")

