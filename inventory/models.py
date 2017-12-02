from core.models import Profile
from products.models import Supplier, Category, Product
from orders.models import Order, OrderLine
from django.db import models


class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier)
    number = models.CharField(max_length=15, default="")
    date_created = models.DateField(auto_now_add=True)
    is_done = models.BooleanField(default=False)
    generated_by = models.ForeignKey(Profile)
    # checks if tapos na


class PurchaseOrderLine(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder)
    product = models.ForeignKey(Product)
    quantity = models.DecimalField(decimal_places=0, max_digits=10)

    @property
    def getsubtotal(self):
        return self.product.unit_cost * self.quantity