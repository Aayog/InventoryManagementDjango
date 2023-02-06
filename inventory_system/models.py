from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    is_empty = models.BooleanField(default=False)