from rest_framework import routers
from .views import *
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .account import activate_account

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'vendors', VendorViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),    
    path('login/', auth_views.LoginView.as_view(template_name='inventory_system/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate'),
]
