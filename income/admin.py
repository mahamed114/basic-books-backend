from django.contrib import admin
from .models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ["income_id", "amount", "owner"]
    list_filter = ["created_at"]
