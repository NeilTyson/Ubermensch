from django.db import models
from core.models import Customer
from products.models import Product


class Order(models.Model):

    customer = models.ForeignKey(Customer)
    inspector_report_no = models.CharField(max_length=15, default='N/A')

    # is_pending means kung naapprove na ba yung order
    is_pending = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)

    PAYMENT_OPTIONS = (
        ('50-40-10', '50-40-10'),
        ('50-30-20', '50-30-20'),
        ('Full Payment', 'Full Payment')
    )

    payment_terms = models.CharField(max_length=40, choices=PAYMENT_OPTIONS, default='0')
    delivery_terms = models.CharField(max_length=1000, default='N/A')
    warranty = models.DecimalField(decimal_places=0, max_digits=5, default='0')
    completion = models.DecimalField(decimal_places=0, max_digits=5, default='0')

    # fields for the order status
    # puro boolean to

    is_accredited = models.BooleanField(default=False)
    has_project_requirements = models.BooleanField(default=False)
    had_canvassed_suppliers = models.BooleanField(default=False)
    has_contract = models.BooleanField(default=False)
    has_retrieved_supplies = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_installed = models.BooleanField(default=False)
    is_under_maintenance = models.BooleanField(default=False)


class OrderLine(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.DecimalField(decimal_places=0, max_digits=10)
