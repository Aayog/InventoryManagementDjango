from rest_framework import viewsets, permissions, renderers
from .models import *
from .serializers import *
from inventory_system.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # only if authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['vendor', 'name', 'category', 'is_empty']
    search_fields = ['=name', 'name']
    ordering_fields = ['name', 'category', 'vendor']
    ordering = ['id']

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.stock == 0:
            instance.is_empty = True
            instance.save()
        elif instance.stock > 0:
            instance.is_empty = False
            instance.save()
            # move to save method models.py to be same with admin
# Signal
# queryset
# 
#   
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAdminUser]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]