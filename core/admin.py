from django.contrib import admin

# Register your models here.
from core.models import Profile, Customer

admin.site.register(Profile)
admin.site.register(Customer)