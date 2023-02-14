from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.sites.shortcuts import get_current_site

class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self) -> str:
        return self.name
    
    def __unicode__(self):
        return self.name
        

class Address(models.Model):
    street_address = models.CharField(max_length=100)
    province = models.CharField(max_length=30)
    district = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=255, default='Nepal')

    def __str__(self) -> str:
        return f'{self.street_address}, {self.district}'
    
    def __unicode__(self):
        return f'{self.street_address}, {self.district}'
        
    
    @staticmethod
    def autocomplete_search_fields():
        return 'name', 'district'

    class Meta:
        verbose_name_plural = "Addresses"

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=20)
    location = models.ForeignKey(Address, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name
    
    def __unicode__(self):
        return self.name
        
# custm login/signup through email verication (login only if verified)

class CustomUserManager(UserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        user.is_active = False
        current_site = get_current_site(request)
        subject = 'Activate Your MySite Account'
        message = render_to_string('account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        return HttpResponse('Please confirm your email address to complete the registration')
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class Customer(AbstractBaseUser):
    phone_num = models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)    
    objects = CustomUserManager()
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = [
        'first_name', 'last_name'
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
  
    def set_is_superuser(self, value):
        self.is_superuser = value
        self.save()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
        
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
    
    def save(self, *args, **kwarg):
        if self.stock == 0:
            self.is_empty = True
        else:
            self.is_empty = False
        super().save(*args, **kwarg)
    
    
# in save method: once order placed decrease stock/quantity

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
    total_price = models.FloatField() #Decimal field
    shipping_address = models.CharField(max_length=255)
    date_ordered = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.customer
    
    def save(self, *args, **kwarg):
        current_status = Order.objects.all(id=self.id).status
        super().save(*args, **kwarg)
        if self.status == 'placed':
            for product in self.products.all():
                product.stock -= product.quantity
                product.save()

        if current_status == 'placed' and self.status == 'cancelled':
            for order_product in self.orderproduct_set.all():
                order_product.product.stock += order_product.quantity
                product.save()
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        else:
            return self.queryset.filter(customer__user=user)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # price = models.FloatField()
    quantity = models.PositiveIntegerField()