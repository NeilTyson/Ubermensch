from django.contrib import admin
from inventory.models import PurchaseOrder, PurchaseOrderLine, RequestedSupply

# Register your models here.


admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderLine)
admin.site.register(RequestedSupply)