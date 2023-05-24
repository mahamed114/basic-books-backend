from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["prod_id", "item_name", "owner"]
    list_filter = ["create_at"]
