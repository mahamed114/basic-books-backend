from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from accounts.models import Employee, Customer
from products.models import Product
from .models import Income
from .serializers import IncomeSerializer


class IncomeCreateListView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_employee == False:
            return Income.objects.filter(owner=user)

        else:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            return Income.objects.filter(owner=organisation)

    def perform_create(self, serializer):
        user = self.request.user

        product_name = self.request.query_params.get("product") or None
        customer_name = self.request.query_params.get("customer") or None

        if user.is_employee == False:
            products_query = Product.objects.filter(owner=user)
            product = products_query.filter(item_slug=product_name).first()

            customers_query = Customer.objects.filter(owner=user)
            customer = customers_query.filter(cus_slug=customer_name).first()

            serializer.save(owner=user, product=product, customer=customer)
            return super().perform_create(serializer)

        else:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for

            products_query = Product.objects.filter(owner=organisation)
            product = products_query.filter(item_slug=product_name).first()

            customers_query = Customer.objects.filter(owner=organisation)
            customer = customers_query.filter(cus_slug=customer_name).first()

            serializer.save(owner=organisation, product=product, customer=customer)
            return super().perform_create(serializer)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class IncomeRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user

        if user.is_employee == True:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            Income.objects.filter(owner=organisation)

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
            salesorder = Income.objects.filter(owner=organisation)

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
