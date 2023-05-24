from rest_framework import serializers

from .models import Income


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = [
            "id",
            "income_id",
            "created_at",
            "income_type",
            "quantity",
            "amount",
            "tax",
            "income_customer",
            "income_product",
            "product",
            "customer",
        ]
