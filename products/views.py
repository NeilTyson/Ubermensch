from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


# TODO
from products.forms import ProductForm, SupplierForm, CategoryForm
from products.models import Product, Supplier, Category


@login_required
def index(request):

    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'products/index.html', context)


@login_required
def category_view(request):

    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'products/categories.html', context)


@login_required
def suppliers(request):

    supps = Supplier.objects.all()

    context = {
        'suppliers': supps
    }

    return render(request, 'products/suppliers.html', context)


@login_required
def create_product(request):
    form = ProductForm(request.POST or None)

    products = Product.objects.all()

    if form.is_valid():
        product = form.save(commit=False)

        supplier = request.POST["supplier"]
        unit_cost = float(request.POST["unit_cost"])

        selling_price = unit_cost * .1 + unit_cost
        product.selling_price = selling_price
        product.save()
        product.supplier.add(supplier)

        messages.success(request, "Product added successfully")
        return render(request, 'products/index.html', {'products': products})

    context = {'form': form}

    return render(request, 'products/create_product.html', context)


@login_required
def add_supplier(request):
    form = SupplierForm(request.POST or None)

    s = Supplier.objects.all()

    if form.is_valid():
        supplier = form.save(commit=False)
        supplier.save()

        messages.success(request, "Supplier added successfully")
        return render(request, 'products/suppliers.html', {'suppliers': s})

    context = {'form': form}

    return render(request, 'products/add_supplier.html', context)


@login_required
def add_category(request):
    form = CategoryForm(request.POST or None)

    c = Category.objects.all()

    if form.is_valid():
        category = form.save(commit=False)
        category.save()

        messages.success(request, "Category added successfully")
        return render(request, 'products/categories.html', {'categories': c})

    context = {'form': form}

    return render(request, 'products/add_category.html', context)


