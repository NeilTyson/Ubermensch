
from django.db import models

# Create your models here.
from core.models import Customer, Profile
from orders.models import Order


class Schedule(models.Model):

    name = models.CharField(max_length=250)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    description = models.CharField(max_length=1000)
    order = models.ForeignKey(Order)
    involved_people = models.ManyToManyField(Profile)

    def __str__(self):
        return self.name
