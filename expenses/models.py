import random
from django.db import models
import uuid as uuid_lib

from accounts.models import User
from products.models import Product
from accounts.models import Vendor


random_id = random.randint(1000000, 9999999)


class Expenses(models.Model):
    id = models.UUIDField(default=uuid_lib.uuid4, unique=True, primary_key=True)
    expense_id = models.CharField(default=random_id, max_length=14)
    created_at = models.DateField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    expense_type = models.CharField(max_length=50)
    expenses_vendor = models.CharField(max_length=50, blank=True)
    expenses_product = models.CharField(max_length=50, blank=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="product_expenses",
        blank=True,
        null=True,
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        related_name="vendor_expenses",
        blank=True,
        null=True,
    )
    quantity = models.DecimalField(max_digits=3, decimal_places=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return str(self.expense_id)

    class Meta:
        ordering = ["-created_at"]
