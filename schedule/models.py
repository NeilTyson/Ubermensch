from datetime import datetime
from django.utils import timezone

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

    @property
    def is_past_today(self):
        naive = self.end_date.replace(tzinfo=None)

        return naive < datetime.now()

    @property
    def is_on_going(self):
        start_date = self.start_date.replace(tzinfo=None)
        end_date = self.end_date.replace(tzinfo=None)

        return start_date <= datetime.now() <= end_date

    @property
    def is_coming_up(self):
        start_date = self.start_date.replace(tzinfo=None)

        return start_date > datetime.now()
