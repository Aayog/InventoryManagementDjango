from django.contrib import admin
from .models import Product, Order, OrderProduct, Vendor, Address, Category, Customer
from django.contrib.auth.admin import UserAdmin
from .forms import CustomerCreationForm, CustomerChangeForm

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    list_filter = ('stock',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_ordered', 'status')
    list_filter = ('date_ordered', 'status')

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity')

class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm

    model = Customer

    list_display = ('email', 'is_active', 'is_superuser',)
    list_filter = ('is_active', 'is_superuser')
    filter_horizontal = []
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active',)}),
        # ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register([Vendor, Category, Address])
admin.site.register(Customer, CustomerAdmin)