from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, redirect
from inventory.models import Product, Supplier, Category, Order, OrderLine
from inventory.models import PurchaseOrder, PurchaseOrderLine
from django.core import serializers
from django.http import JsonResponse, Http404, HttpResponse
from core.models import Profile
from Ubermensch import helper
import random
import json
from collections import Counter


@login_required
def index(request):

    products = Product.objects.all()
    all_po = PurchaseOrder.objects.all()

    context = {
        'products': products,
        'purchase_orders': all_po
    }
    return render(request, 'inventory/index.html', context)


@login_required
def view_all_po(request):
    all_po = PurchaseOrder.objects.all()
    return render(request, 'inventory/view_all_po.html', {'purchase_orders': all_po})


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

def get_products_using_supplier(request):

    supplier_id = request.POST['supplier_id']
    supplier = Supplier.objects.get(id=supplier_id)
    products = Product.objects.filter(supplier=supplier)
    serialized = serializers.serialize('json', products)
    data = {'products': serialized}

    return JsonResponse(data)


def generate_po(request):
    number = random.randint(1, 999999)
    po_no = "PO-" + str(number)

    while helper.check_duplicate_numbers(po_no, 'purchase'):
        number = random.randint(1, 999999)
        po_no = "PO-" + str(number)


    request_body = request.body
    print(request_body)
    data = json.loads(request_body)
    supplier_id = data['supplier_id']
    print (supplier_id)
    po_cart = data['po_cart']
    profile = Profile.objects.get(user=request.user)
    PurchaseOrder.objects.create(
        supplier=Supplier.objects.get(id=supplier_id),
        generated_by=profile,
        number=po_no
    )
    po = PurchaseOrder.objects.latest("id")
    for item in po_cart:
            PurchaseOrderLine.objects.create(
                purchase_order=po,
                product=Product.objects.get(id=item['id']),
                quantity=item['qty']
            )
    return HttpResponse("success")


def view_po(request, po_id):
    po_details = PurchaseOrder.objects.get(id=po_id)
    orderLine = PurchaseOrderLine.objects.filter(purchase_order=po_details)
    total = 0
    for line in orderLine:
        total+=line.quantity * line.product.unit_cost
    context = {
        'purchase_order': po_details,
        'purchase_orderline': orderLine,
        'total': total,
    }
    return render(request, 'inventory/purchase_order.html', context)


def confirm_product_retrieval(request, po_id):
    po_details = PurchaseOrder.objects.get(id=po_id)
    orderLine = PurchaseOrderLine.objects.filter(purchase_order=po_details)
    for line in orderLine:
        product_reference = line.product
        product = Product.objects.get(id=product_reference.pk)
        product.quantity_in_stock += line.quantity
        product.save()
    po_details.is_done = True
    po_details.save()
    return HttpResponse("Success")



@login_required
def request_products(request):

    current_order = Order.objects.get(id=request.GET['order'])
    orders = Order.objects.filter(has_contract_done=True, has_retrieved_supplies=False)

    supplies = []

    for order in orders:
        for line in order.orderline_set.all():
            supply = {
                'id': line.product.id,
                'quantity': line.quantity
            }

            supplies.append(supply)
        order.has_requested_products = True
        order.save()

    supplies = helper.merge_list(supplies)

    profile = Profile.objects.get(user=request.user)


    # supplier_list = []
    #
    # for supplier in Supplier.objects.all():
    #     requested_supplies = []
    #     supplier_list.append( {"supplier" : supplier, "requested_supplies" : requested_supplies})
    #
    #     for product in supplier.product_set.all():
    #         for requested_supply in product.requestedsupply_set.all():
    #             requested_supplies.append(requested_supply)

    temp_suppliers = []
    for x in supplies:
        product = Product.objects.get(id=x['id'])
        supplier = product.supplier.all()[0]

        if supplier not in temp_suppliers:
            temp_suppliers.append(supplier)

    for x in temp_suppliers:

        number = random.randint(1, 999999)
        po_no = "PO-" + str(number)

        while helper.check_duplicate_numbers(po_no, 'purchase'):
            number = random.randint(1, 999999)
            po_no = "PO-" + str(number)

        PurchaseOrder.objects.create(
            number=po_no,
            generated_by=profile,
            supplier=x
        )

        po = PurchaseOrder.objects.latest('id')

        for a in supplies:
            product = Product.objects.get(id=a['id'])

            if product.supplier.all()[0] == po.supplier:

                PurchaseOrderLine.objects.create(
                    purchase_order=po,
                    product=product,
                    quantity=a['quantity']
                )

        for order in orders:
            order.has_retrieved_supplies = True
            order.status = 'Delivery'
            order.save()


    messages.success(request, 'Supplies requested')
    return redirect('orders:product_retrieval', order_id=current_order.id)


@login_required
def po_list(request):
    purchase_orders = PurchaseOrder.objects.all()

    context = {
        'purchase_orders': purchase_orders
    }

    return render(request, 'inventory/po-list.html', context)
