from django.contrib import admin

# Register your models here.
from products.models import Supplier, Product

admin.site.register(Supplier)
admin.site.register(Product)