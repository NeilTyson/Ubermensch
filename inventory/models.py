from products.models import Supplier, Category, Product
from orders.models import Order, OrderLine
from django.db import models


class RequestedSupplies(models.Model):
    supplier = models.ForeignKey(Supplier)
    product = models.ForeignKey(Product)
    quantity = models.DecimalField(max_digits=5, decimal_places=0)

    # checks if tapos na
    is_done = models.BooleanField(default=False)
