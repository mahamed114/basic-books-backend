from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "prod_id",
            "create_at",
            "item_type",
            "item_unit",
            "item_name",
            "item_slug",
            "item_description",
            "item_parchase_price",
            "item_sale_price",
        ]
