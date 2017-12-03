from django.contrib import admin

# Register your models here.
from maintenance.models import MaintenanceContract, TroubleTicket

admin.site.register(MaintenanceContract)
admin.site.register(TroubleTicket)