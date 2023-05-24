from django.urls import path
from .views import *

urlpatterns = [
    path(
        "",
        ExpensesCreateListView.as_view(),
        name="create-or-list-expenses",
    ),
    path(
        "<pk>/",
        ExpensesRetrieveUpdateDeleteView.as_view(),
        name="update-expenses",
    ),
]
