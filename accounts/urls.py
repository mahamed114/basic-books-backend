from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


from .views import *

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("verify/", VerifyOTP.as_view(), name="verify"),
    path("logout/", User_logout, name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("profile/", OrganisationProfileView.as_view(), name="profile"),
    path(
        "customers/", CustomerCreateListView.as_view(), name="create-or-list-customers"
    ),
    path(
        "customers/<pk>/",
        CustomerRetrieveUpdateDeleteView.as_view(),
        name="update-customer",
    ),
    path("vendors/", VendorCreateListView.as_view(), name="create-or-list-vendors"),
    path(
        "vendors/<pk>/", VendorRetrieveUpdateDeleteView.as_view(), name="update-vendor"
    ),
    path("employees/", EmployeeCreateListView.as_view(), name="invite-employee"),
]
