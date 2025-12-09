from django.db import models
from django.contrib.auth.models import User

class Requisition(models.Model):
    name = models.CharField(max_length=255)
    icon_url = models.URLField(null=True, blank=True)   # Supabase

    def __str__(self):
        return self.name


class Product(models.Model):
    requisition = models.ForeignKey(Requisition, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    # URL no Supabase
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
