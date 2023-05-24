from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "organisation_name"]
    list_filter = ["date_joined"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["user", "employee_name", "employee_for"]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["cus_id", "cus_name", "owner"]
    list_filter = ["created_at"]


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["ven_id", "ven_name", "owner"]
    list_filter = ["created_at"]
