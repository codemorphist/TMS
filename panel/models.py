from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from panel.forms import OrderForm
from users.models import PanelUser


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('panel:category', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('panel:product', kwargs={'pk': self.pk})

    def get_order_form(self):
        return OrderForm(product=self)

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    client = models.ForeignKey(PanelUser, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_total_price(self) -> float:
        return round(self.product.price * self.quantity, 2)