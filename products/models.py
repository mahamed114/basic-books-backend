import random
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid as uuid_lib

from accounts.models import User

product_id = random.randint(1000000, 9999999)


class Product(models.Model):
    id = models.UUIDField(default=uuid_lib.uuid4, unique=True, primary_key=True)
    prod_id = models.CharField(default=product_id, max_length=14)
    create_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    item_type = models.CharField(max_length=7)
    item_unit = models.CharField(max_length=15)
    item_name = models.CharField(max_length=100)
    item_slug = models.CharField(max_length=100, blank=True)
    item_description = models.CharField(max_length=150)
    item_parchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return str(self.item_name)

    class Meta:
        ordering = ["-create_at"]
