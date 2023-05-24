from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request


from accounts.models import Employee
from .models import Product
from .serializers import ProductSerializer


class ProductListCreateView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_employee == True:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            return Product.objects.filter(owner=organisation)

        else:
            return Product.objects.filter(owner=user)

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


class ProductRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user

        if user.is_employee == True:
            query_employee = Employee.objects.filter(user=user).first()
            organisation = query_employee.employee_for
            Product.objects.filter(owner=organisation)

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
            product = Product.objects.filter(owner=organisation)

            serializer.save(product=product)
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
