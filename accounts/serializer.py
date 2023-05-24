from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response


from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "otp",
            "date_joined",
            "is_employee",
            "owner_name",
            "owner_mobile",
            "organisation_name",
            "organisation_country",
            "organisation_address",
            "organisation_phone",
            "organisation_email",
            "default_currency",
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "employee_for",
            "employee_name",
            "employee_user_email",
        ]


class CustomerSerializer(serializers.ModelSerializer):
    cus_name = serializers.CharField(max_length=50)

    class Meta:
        model = Customer
        fields = [
            "id",
            "cus_id",
            "cus_type",
            "cus_name",
            "cus_slug",
            "cus_email",
            "cus_mobile",
            "cus_company",
        ]


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "id",
            "ven_id",
            "ven_name",
            "ven_slug",
            "ven_email",
            "ven_mobile",
            "ven_company",
        ]


class SignUpViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "organisation_name", "is_verified"]

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            return Response(
                data="Email has already been used", status=status.HTTP_201_CREATED
            )

        return super().validate(attrs)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.save()

        Token.objects.create(user=user)

        return user


class SignInViewSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["email"]


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
