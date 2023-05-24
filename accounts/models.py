from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
import uuid as uuid_lib
import random


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(
        default=uuid_lib.uuid4, unique=True, primary_key=True, editable=False
    )
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="date joined")
    email = models.EmailField(max_length=80, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_employee = models.BooleanField(default=False)
    owner_name = models.CharField(max_length=100, blank=True)
    owner_mobile = models.CharField(max_length=14, blank=True)
    organisation_name = models.CharField(max_length=100, blank=True)
    organisation_country = models.CharField(max_length=50, blank=True, null=True)
    organisation_address = models.CharField(max_length=120, blank=True, null=True)
    organisation_phone = models.CharField(max_length=14, blank=True)
    organisation_email = models.CharField(max_length=50, blank=True)
    default_currency = models.CharField(
        max_length=3, default="USD", blank=True, null=True
    )

    objects = CustomUserManager()
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Employee(models.Model):
    user = models.OneToOneField(User, related_name="Employee", on_delete=models.CASCADE)
    employee_for = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, related_name="employees"
    )
    employee_user_email = models.CharField(max_length=100, blank=True)
    employee_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.employee_name


customer_id = random.randint(1000000, 9999999)


class Customer(models.Model):
    id = models.UUIDField(default=uuid_lib.uuid4, unique=True, primary_key=True)
    cus_id = models.CharField(default=customer_id, max_length=14)
    cus_type = models.CharField(max_length=50)
    cus_name = models.CharField(max_length=100)
    cus_slug = models.CharField(max_length=100, blank=True)
    cus_email = models.CharField(max_length=50, blank=True, null=True)
    cus_mobile = models.CharField(max_length=14, blank=True, null=True)
    cus_company = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.cus_name

    class Meta:
        ordering = ["-created_at"]


vendor_id = random.randint(1000000, 9999999)


class Vendor(models.Model):
    id = models.UUIDField(default=uuid_lib.uuid4, unique=True, primary_key=True)
    ven_id = models.CharField(default=customer_id, max_length=14)
    ven_name = models.CharField(max_length=100)
    ven_slug = models.CharField(max_length=100, blank=True)
    ven_email = models.CharField(max_length=50, blank=True, null=True)
    ven_mobile = models.CharField(max_length=14, blank=True, null=True)
    ven_company = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vendors")

    def __str__(self) -> str:
        return self.ven_name

    class Meta:
        ordering = ["-created_at"]
