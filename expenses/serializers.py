from rest_framework import serializers

from .models import Expenses


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = [
            "id",
            "expense_id",
            "created_at",
            "expense_type",
            "quantity",
            "amount",
            "tax",
            "expenses_product",
            "expenses_vendor",
            "product",
            "vendor",
        ]
