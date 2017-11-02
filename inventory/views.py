from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from inventory.models import Product, Supplier, Category


@login_required
def index(request):

    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'inventory/index.html', context)