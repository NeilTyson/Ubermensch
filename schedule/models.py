
from django.db import models

# Create your models here.
from core.models import Customer


class Schedule(models.Model):

    name = models.CharField(max_length=250)
    deadline_date = models.DateField()
    deadline_time = models.TimeField()
    is_completed = models.BooleanField(default=False)
    description = models.CharField(max_length=1000, default="")
    customer = models.ForeignKey(Customer)

    INVENTORY = 'Inventory'
    SALES = 'Sales'
    PROCUREMENT = 'Procurement'
    ACCOUNTING = 'Accounting'
    TECHNICAL = 'Technical'
    ADMIN = 'Admin'

    DEPARTMENT_CHOICES = (
        (INVENTORY, "Inventory"),
        (SALES, "Sales"),
        (PROCUREMENT, "Procurement"),
        (ACCOUNTING, "Accounting"),
        (TECHNICAL, "Technical"),
        (ADMIN, "Admin")
    )

    responsible_department = models.CharField(
        max_length=30,
        choices=DEPARTMENT_CHOICES,
        default=SALES
    )
