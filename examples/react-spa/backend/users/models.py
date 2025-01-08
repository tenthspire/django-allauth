from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('merchant', 'Merchant'),
        ('customer', 'Customer'),
        ('developer','Developer'),
    )
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default='customer'
    )

product_type = (
    ('electronic','Electronic'),
    ('grocary','Grocary'),
    ('medicine','Medicine'),
    ('stationary','Stationary'),
)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
    discounted_price = models.DecimalField(max_digits=5,decimal_places=2)
    type = models.CharField(max_length=20,choices=product_type,default='electronic')

    def __str__(self):
        return self.name