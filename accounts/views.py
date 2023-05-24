from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, status, mixins
from django.contrib.auth import authenticate, logout
from django.shortcuts import get_object_or_404

from .models import *
from .serializer import *
from .tokens import create_jwt_pair_for_user
from .emails import send_otp_via_email, send_invite_via_email


class SignUpView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = SignUpViewSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data["email"])
                response = {
                    "status": 201,
                    "message": "User Created Successfully. Check email.",
                    "data": serializer.data,
                }
                return Response(data=response, status=status.HTTP_201_CREATED)

            response = {
                "status": 400,
                "message": "something went wrong",
                "data": serializer.errors,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Exception: {e}")


class SignInView(APIView):
    def post(self, request):

        data = request.data
        serializer = SignInViewSerializer(data=data)

        if serializer.is_valid():
            email = serializer.data["email"]

            user = User.objects.filter(email=email)
            if not user.exists():
                return Response(
                    {
                        "status": 400,
                        "message": "Something went wront!",
                        "data": "Invalid Email",
                    }
                )

            send_otp_via_email(email)
            user = user.first()
            Token.objects.get_or_create(user=user)

            user.save()
            response = {
                "status": 200,
                "message": "OTP successfully sent. check your email",
                "data": {},
            }
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(
                {
                    "status": 400,
                    "message": "Something is not working",
                    "data": serializer.errors,
                }
            )


class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyOTPSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data["email"]
                otp = serializer.data["otp"]

                user = authenticate(email=email)

                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response(
                        {
                            "status": 400,
                            "message": "Something went wrong!",
                            "data": "Invalid Email",
                        }
                    )

                if user[0].otp != otp:
                    return Response(
                        {
                            "status": 400,
                            "message": "Something went wrong!",
                            "data": "Invalid OTP",
                        }
                    )

                user = user.first()
                user.is_verified = True
                user.save()
                tokens = create_jwt_pair_for_user(user)

                response = {
                    "status": 200,
                    "message": "Account verified and loggedin successfully.",
                    "data": tokens,
                }
                return Response(data=response, status=status.HTTP_200_OK)

            return Response(
                {
                    "status": 400,
                    "message": "",
                    "data": serializer.errors,
                }
            )

        except Exception as e:
            print(f"Exception: {e}")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):

    request.user.auth_token.delete()

    logout(request)

    return Response("User Logged out successfully")


class OrganisationProfileView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        email = self.request.user.email
        theuser = User.objects.filter(email=email).first()
        if theuser.is_employee == False:
            obj = get_object_or_404(User, email=email)
            return obj
        return None

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CustomerCreateListView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_employee == True:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            return Customer.objects.filter(owner=organisation)

        else:
            return Customer.objects.filter(owner=user)

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_employee == True:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            serializer.save(owner=organisation)
            return super().perform_create(serializer)

        else:
            serializer.save(owner=user)
            return super().perform_create(serializer)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustomerRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user

        if user.is_employee == True:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            customers = Customer.objects.filter(owner=organisation)

            serializer.save(customers=customers)
            return super().perform_update(serializer)
        else:
            serializer.save()
            return super().perform_update(serializer)

    def perform_destory(self, serializer):
        user = self.request.user

        if user.is_employee == True:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            customer = Customer.objects.filter(owner=organisation)

            serializer.save(customer=customer)
            return super().perform_destory(serializer)
        else:
            serializer.save()
            return super().perform_destory(serializer)

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class VendorCreateListView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_employee == True:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            return Vendor.objects.filter(owner=organisation)

        else:
            return Vendor.objects.filter(owner=user)

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_employee == True:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            serializer.save(owner=organisation)
            return super().perform_create(serializer)

        else:
            serializer.save(owner=user)
            return super().perform_create(serializer)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VendorRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user

        if user.is_employee == True:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            vendor = Vendor.objects.filter(owner=organisation)

            serializer.save(vendor=vendor)
            return super().perform_update(serializer)
        else:
            serializer.save()
            return super().perform_update(serializer)

    def perform_destory(self, serializer):
        user = self.request.user

        if user.is_employee == True:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            vendor = Vendor.objects.filter(owner=organisation)

            serializer.save(vendor=vendor)
            return super().perform_destory(serializer)
        else:
            serializer.save()
            return super().perform_update(serializer)

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EmployeeCreateListView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_employee == False:
            return Employee.objects.filter(employee_for=user)

        else:
            return Response(data="BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        user = self.request.user

        employee_email = self.request.query_params.get("employee_email") or None
        employee_name = self.request.query_params.get("employee_name") or None
        finalemployee_name = employee_name.replace("-", " ")

        try:
            if user.is_employee == False:
                new_user = User.objects.create_user(
                    email=employee_email, is_employee=True
                )
                org_name = user.organisation_name or None

                Employee.objects.create(
                    user=new_user,
                    employee_for=user,
                    employee_user_email=employee_email,
                    employee_name=finalemployee_name,
                )

                send_invite_via_email(
                    email=employee_email, name=finalemployee_name, orgname=org_name
                )

                return Response(
                    data="Invite Sent Successfuly", status=status.HTTP_201_CREATED
                )

            else:

                return Response(data="BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Exception: {e}")

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
