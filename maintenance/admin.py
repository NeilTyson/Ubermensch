from django.contrib import admin

# Register your models here.
from maintenance.models import MaintenanceContract

admin.site.register(MaintenanceContract)