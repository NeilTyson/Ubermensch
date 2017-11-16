from django.db import models

from core.models import Profile
from orders.models import Order


class OrderMaintenance(models.Model):

    order = models.OneToOneField(Order)
    maintenance_contract_no = models.CharField(max_length=10, default='na')
    date_created = models.DateField()
    duration = models.DecimalField(decimal_places=2, max_digits=5)
    price = models.DecimalField(decimal_places=2, max_digits=7)


class TroubleReport(models.Model):
    trouble_report_no = models.CharField(max_length=10, default='na')
    date_requested = models.DateField()
    date_created = models.DateField()
    date_of_visit = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    engineer = models.ForeignKey(Profile)
    complaint = models.TextField(max_length=1500)
    findings = models.TextField(max_length=1500)

