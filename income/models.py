import random
from django.db import models
import uuid as uuid_lib

from accounts.models import User
from products.models import Product
from accounts.models import Customer


random_id = random.randint(1000000, 9999999)


class Income(models.Model):
    id = models.UUIDField(default=uuid_lib.uuid4, unique=True, primary_key=True)
    income_id = models.CharField(default=random_id, max_length=14)
    created_at = models.DateField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incomes")
    income_type = models.CharField(max_length=50)
    income_customer = models.CharField(max_length=50, blank=True)
    income_product = models.CharField(max_length=50, blank=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="product_income",
        blank=True,
        null=True,
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        related_name="customer_income",
        blank=True,
        null=True,
    )
    quantity = models.DecimalField(max_digits=3, decimal_places=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return str(self.income_id)

    class Meta:
        ordering = ["-created_at"]
