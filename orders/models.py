from datetime import datetime

from django.db import models
from core.models import Customer, Profile
from products.models import Product


class Order(models.Model):

    customer = models.ForeignKey(Customer)
    date_created = models.DateField(auto_now_add=True)

    # fields for the order status
    # puro boolean to

    has_project_requirements = models.BooleanField(default=False)
    has_contract = models.BooleanField(default=False)
    has_contract_done = models.BooleanField(default=False)
    has_retrieved_supplies = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_installed = models.BooleanField(default=False)
    is_maintained = models.BooleanField(default=False)

    # schedules
    has_scheduled_engineers = models.BooleanField(default=False)
    has_scheduled_delivery = models.BooleanField(default=False)

    status = models.CharField(max_length=100, default="Contract")

    def __str__(self):
        return str(self.customer)


class InspectorReport(models.Model):
    order = models.OneToOneField(Order)
    inspector_report_no = models.CharField(max_length=15, default='na')
    duration = models.DecimalField(decimal_places=0, max_digits=5, default='0')
    manpower = models.DecimalField(decimal_places=0, max_digits=5, default='0')
    date_created = models.DateTimeField(default=datetime.now)
    generated_by = models.OneToOneField(Profile)


class OrderLine(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.DecimalField(decimal_places=0, max_digits=10)


class OfficialReceipt(models.Model):
    order = models.ForeignKey(Order)
    date_created = models.DateField(default=datetime.now)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    number = models.CharField(max_length=15)
    generated_by = models.ForeignKey(Profile)

class DeliveryReceipt(models.Model):
    order = models.ForeignKey(Order)
    date_created = models.DateField(default=datetime.now)
    generated_by = models.ForeignKey(Profile)
    number = models.CharField(max_length=15)


class Contract(models.Model):
    order = models.OneToOneField(Order)
    number = models.CharField(max_length=15)
    date_created = models.DateTimeField(default=datetime.now)
    generated_by = models.ForeignKey(Profile)

    PAYMENT_OPTIONS = (
        ('50-40-10', '50-40-10'),
        ('50-30-20', '50-30-20'),
        ('Full Payment', 'Full Payment')
    )

    FORM_OF_PAYMENT = (
        ('Check', 'Check'),
        ('Cash', 'Cash')
    )

    first_percentage = models.DecimalField(default=0, decimal_places=0, max_digits=4, null=True)
    second_percentage = models.DecimalField(default=0, decimal_places=0, max_digits=4, null=True)
    third_percentage = models.DecimalField(default=0, decimal_places=0, max_digits=4, null=True)

    payment_terms = models.CharField(max_length=40, choices=PAYMENT_OPTIONS)
    delivery_terms = models.CharField(max_length=1000)
    warranty = models.DecimalField(decimal_places=0, max_digits=5)
    completion = models.DecimalField(decimal_places=0, max_digits=5)
    consumables_fee = models.DecimalField(decimal_places=0, max_digits=5)
    engineering_fee = models.DecimalField(decimal_places=0, max_digits=5)
    installation_fee = models.DecimalField(decimal_places=0, max_digits=5)
    form_of_payment = models.CharField(max_length=30, choices=FORM_OF_PAYMENT, default='Check')


class BillingStatement(models.Model):

    order = models.ForeignKey(Order)
    number = models.CharField(max_length=15)
    date_created = models.DateTimeField(default=datetime.now)
    percentage = models.DecimalField(max_digits=5, decimal_places=0, help_text="In percent")
    item = models.CharField(max_length=1000)
    generated_by = models.ForeignKey(Profile)


class ProgressReport(models.Model):

    order = models.ForeignKey(Order)
    number = models.CharField(max_length=15)
    date_created = models.DateTimeField(default=datetime.now)
    title = models.CharField(max_length=256)
    generated_by = models.ForeignKey(Profile)
    report_progress = models.TextField()

    def __str__(self):
        return str(self.date_created.date())







