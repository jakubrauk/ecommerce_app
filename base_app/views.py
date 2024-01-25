from datetime import datetime

import django_filters.rest_framework
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, filters, permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from base_app.models import Product, ProductCategory, Order, OrderAddress, OrderItem
from base_app.serializers import UserSerializer, GroupSerializer, ProductSerializer, ProductCategorySerializer, \
    OrderSerializer, OrderAddressSerializer, OrderItemSerializer, ProductStatisticsSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'category', 'description', 'price']
    search_fields = ['name', 'category__name', 'description']
    ordering_fields = ['name', 'category__name', 'price']


class ProductsStatistics(ReadOnlyModelViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.from_date = None
        self.to_date = None
        self.count = None

    queryset = OrderItem.objects.all()
    serializer_class = ProductStatisticsSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        from_date = datetime.strptime(self.from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(self.to_date, '%Y-%m-%d').date()
        count = int(self.count)
        return OrderItem.get_product_statistics(from_date, to_date, count)

    def list(self, request, *args, **kwargs):
        self.from_date = request.query_params.get('from_date', None)
        self.to_date = request.query_params.get('to_date', None)
        self.count = request.query_params.get('count', None)
        if not all([self.from_date, self.to_date, self.count]):
            # TODO validate parameters
            # TODO clean parameters
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().list(request, *args, **kwargs)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all().order_by('name')
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.DjangoModelPermissions]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class OrderAddressViewSet(viewsets.ModelViewSet):
    queryset = OrderAddress.objects.all().order_by('city')
    serializer_class = OrderAddressSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().order_by('-order__order_date')
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.DjangoModelPermissions]
