from django.urls import path
from .views import *

urlpatterns = [
    path("", ProductListCreateView.as_view(), name="create-or-list-Products"),
    path("<pk>/", ProductRetrieveUpdateDeleteView.as_view(), name="update-product"),
]
