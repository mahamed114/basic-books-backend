from django.urls import path
from .views import *

urlpatterns = [
    path(
        "",
        IncomeCreateListView.as_view(),
        name="create-or-list-income",
    ),
    path(
        "<pk>/",
        IncomeRetrieveUpdateDeleteView.as_view(),
        name="update-income",
    ),
]
