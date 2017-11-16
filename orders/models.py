from datetime import datetime

from django.db import models
from core.models import Customer
from products.models import Product


class Order(models.Model):

    customer = models.ForeignKey(Customer)
    date_created = models.DateField(auto_now_add=True)

    # fields for the order status
    # puro boolean to

    has_project_requirements = models.BooleanField(default=False)
    has_contract = models.BooleanField(default=False)
    has_retrieved_supplies = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_installed = models.BooleanField(default=False)
    is_maintained = models.BooleanField(default=False)

    # documents
    invoice_no = models.CharField(max_length=10, default='na')
    purchase_order_no = models.CharField(max_length=15, default='na')
    pull_out_slip_no = models.CharField(max_length=15, default='na')


class InspectorReport(models.Model):
    order = models.OneToOneField(Order)
    inspector_report_no = models.CharField(max_length=15, default='na')
    duration = models.DecimalField(decimal_places=0, max_digits=5, default='0')
    manpower = models.DecimalField(decimal_places=0, max_digits=5, default='0')
    date_created = models.DateTimeField(default=datetime.now)


class OrderLine(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.DecimalField(decimal_places=0, max_digits=10)


class OfficialReceipt(models.Model):
    order = models.ForeignKey(Order)
    date_created = models.DateField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)


class DeliveryReceipt(models.Model):
    order = models.ForeignKey(Order)
    date_created = models.DateField()


class Contract(models.Model):
    order = models.OneToOneField(Order)
    date_created = models.DateTimeField(default=datetime.now)

    PAYMENT_OPTIONS = (
        ('50-40-10', '50-40-10'),
        ('50-30-20', '50-30-20'),
        ('Full Payment', 'Full Payment')
    )

    payment_terms = models.CharField(max_length=40, choices=PAYMENT_OPTIONS)
    delivery_terms = models.CharField(max_length=1000)
    warranty = models.DecimalField(decimal_places=0, max_digits=5)
    completion = models.DecimalField(decimal_places=0, max_digits=5)
    consumables_fee = models.DecimalField(decimal_places=2, max_digits=5)
    engineering_fee = models.DecimalField(decimal_places=2, max_digits=5)
    installation_fee = models.DecimalField(decimal_places=2, max_digits=5)







