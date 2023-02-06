from rest_framework import viewsets, permissions, renderers
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product
from .serializers import ProductSerializer
from inventory_system.permissions import IsOwnerOrReadOnly
from django.core.mail import send_mail

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Instead of waiting on it to be zero, sending a notification if it's less than 3
        if int(self.request.data['stock']) <= 3:
            send_mail(
                'Stock Empty Notification',
                f'The stock of product {self.request.data["name"]} is empty.',
                'rudahabmar@gmail.com',
                ['1aayogkoirala@gmail.com'],
                fail_silently=False,
            )
        serializer.save()