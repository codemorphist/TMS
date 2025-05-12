from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from users.models import PanelUser


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products', null=True)
    description = models.TextField(blank=True)
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    provider = models.ForeignKey(PanelUser, on_delete=models.CASCADE, related_name='products', null=True)

    def get_absolute_url(self):
        return reverse('product', args=(self.pk,))


class CatalogProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
