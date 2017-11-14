from django.contrib import admin

# Register your models here.
from orders.models import Order, OrderLine, InspectorReport

admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(InspectorReport)
