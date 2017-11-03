from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=250)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    INVENTORY = 'Inventory'
    SALES = 'Sales'
    PROCUREMENT = 'Procurement'
    ACCOUNTING = 'Accounting'
    TECHNICAL = 'Technical'
    ADMIN = 'Admin'

    USER_TYPE_CHOICES = (
        (INVENTORY, "Inventory"),
        (SALES, "Sales"),
        (PROCUREMENT, "Procurement"),
        (ACCOUNTING, "Accounting"),
        (TECHNICAL, "Technical"),
        (ADMIN, "Admin")
    )

    user_type = models.CharField(
        max_length=50,
        choices=USER_TYPE_CHOICES,
        default=SALES
    )

    def get_user_type(self):
        return self.user_type

    # def __str__(self):
    #     return self.first_name + " " + self.last_name + " - " + self.user_type

    def __str__(self):
        return self.user.username

    def set_password(self, raw_password):
        self.user.set_password(raw_password)


class Customer(models.Model):

    company_name = models.CharField(max_length=250, unique=True)
    contact_first_name = models.CharField(max_length=50)
    contact_last_name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=20)
    email_address = models.EmailField()
    address = models.CharField(max_length=400)

    # kung tanggap nitong customer na to ang digicom
    is_accredited = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name


