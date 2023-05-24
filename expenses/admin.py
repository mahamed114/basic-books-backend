from django.contrib import admin
from .models import Expenses


@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ["expense_id", "amount", "owner"]
    list_filter = ["created_at"]
