from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=250)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    INVENTORY = 'Inventory'
    PROCUREMENT = 'Procurement'
    ACCOUNTING = 'Accounting'
    TECHNICAL = 'Technical'
    ADMIN = 'Admin'
    ENGINEER = 'Engineer'

    USER_TYPE_CHOICES = (
        (INVENTORY, "Inventory"),
        (PROCUREMENT, "Procurement"),
        (ACCOUNTING, "Accounting"),
        (TECHNICAL, "Technical"),
        (ADMIN, "Admin"),
        (ENGINEER, "Engineer"),
        ("SALES", "Sales")
    )

    user_type = models.CharField(
        max_length=50,
        choices=USER_TYPE_CHOICES,
        default=PROCUREMENT
    )

    def get_user_type(self):
        return self.user_type

    def __str__(self):
        return self.user.username

    def set_password(self, raw_password):
        self.user.set_password(raw_password)

    def __unicode__(self):
        return self.user.first_name


class Customer(models.Model):

    company_name = models.CharField(max_length=250, unique=True)
    contact_first_name = models.CharField(max_length=50)
    contact_last_name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=20)
    email_address = models.EmailField()
    address = models.CharField(max_length=400)

    def __str__(self):
        return self.company_name


