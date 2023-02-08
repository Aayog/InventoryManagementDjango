from django.contrib import admin
from .models import Product, Order, OrderProduct, Vendor, Address, Category, Customer

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    list_filter = ('stock',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_ordered', 'status')
    list_filter = ('date_ordered', 'status')

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity')

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register([Vendor, Category, Address, Customer])