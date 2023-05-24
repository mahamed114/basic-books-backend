from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/auth/", include("accounts.urls")),
    path("books/products/", include("products.urls")),
    path("books/income/", include("income.urls")),
    path("books/expenses/", include("expenses.urls")),
]
