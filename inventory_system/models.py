from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self) -> str:
        return self.name

class Address(models.Model):
    street_address = models.CharField(max_length=100)
    province = models.CharField(max_length=30)
    district = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=255, default='Nepal')

    def __str__(self) -> str:
        return f'{self.street_address}, {self.district}'
    
    class Meta:
        verbose_name_plural = "Addresses"

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=20)
    location = models.ForeignKey(Address, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name

class Customer(models.Model):
    phone_num = models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f'{self.first_name}'

class Product(models.Model):
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField() #how many in stock
    is_empty = models.BooleanField(default=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cost_price = models.FloatField() #price bought from the vendor (price before profit)
    price = models.FloatField() #price it was sold at
    stock_threshold = models.PositiveIntegerField(default=3)
    def __str__(self) -> str:
        return self.name
    

class Order(models.Model):
    choices = [
        ('processing', 'Processing'),
        ('placed', 'Placed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    products = models.ManyToManyField(Product, through='OrderProduct')
    status = models.CharField(choices=choices, max_length=10)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.FloatField()
    shipping_address = models.CharField(max_length=255)
    date_ordered = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.customer

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # price = models.FloatField()
    quantity = models.PositiveIntegerField()