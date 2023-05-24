from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request


from accounts.models import Employee, Vendor
from products.models import Product

from .models import Expenses
from .serializers import ExpensesSerializer


class ExpensesCreateListView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_employee == False:
            return Expenses.objects.filter(owner=user)

        else:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            return Expenses.objects.filter(owner=organisation)

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_employee == False:
            product_name = self.request.query_params.get("product") or None
            vendor_name = self.request.query_params.get("vendor") or None

            products_query = Product.objects.filter(owner=user)
            product = products_query.filter(item_slug=product_name).first()

            vendors_query = Vendor.objects.filter(owner=user)
            vendor = vendors_query.filter(ven_slug=vendor_name).first()

            serializer.save(owner=user, product=product, vendor=vendor)
            return super().perform_create(serializer)

        else:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for

            products_query = Product.objects.filter(owner=organisation)
            product = products_query.filter(item_slug=product_name).first()

            vendors_query = Vendor.objects.filter(owner=organisation)
            vendor = vendors_query.filter(ven_slug=vendor_name).first()

            serializer.save(owner=organisation, product=product, vendor=vendor)
            return super().perform_create(serializer)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExpensesRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = ExpensesSerializer
    queryset = Expenses.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user

        if user.is_employee == True:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            Expenses.objects.filter(owner=organisation)

            serializer.save()
            return super().perform_update(serializer)
        else:
            serializer.save()
            return super().perform_update(serializer)

    def perform_destory(self, serializer):
        user = self.request.user

        if user.is_employee == True:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            salesorder = Expenses.objects.filter(owner=organisation)

            serializer.save(salesorder=salesorder)
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
