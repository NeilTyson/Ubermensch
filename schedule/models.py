
from django.db import models

# Create your models here.
from core.models import Customer, Profile


class Schedule(models.Model):

    name = models.CharField(max_length=250)
    deadline_date = models.DateField()
    deadline_time = models.TimeField()
    is_completed = models.BooleanField(default=False)
    description = models.CharField(max_length=1000, default="")
    customer = models.ForeignKey(Customer)
    involved_people = models.ManyToManyField(Profile)