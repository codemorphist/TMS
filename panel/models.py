from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from users.models import PanelUser


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True,
                                 related_name='products')
    description = models.TextField(blank=True)
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0.0)])
    provider = models.ForeignKey(PanelUser, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='products')

    def get_absolute_url(self):
        return reverse('panel:product', args=(self.pk,))

    def __str__(self):
        return f'{self.name}'


class CatalogProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])

    def get_absolute_url(self):
        return reverse('panel:catalog-product', args=(self.pk,))

    def __str__(self):
        return f'{self.product.name}'


class OrderStatus(models.TextChoices):
    IN_PROGRESS = 'in_progress', _('In Progress')
    CANCELED = 'canceled', _('Canceled')
    COMPLETED = 'completed', _('Completed')


class ClientOrder(models.Model):
    user = models.ForeignKey(PanelUser, on_delete=models.CASCADE)
    product = models.ForeignKey(CatalogProduct, on_delete=models.CASCADE)
    count = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    status = models.CharField(choices=OrderStatus.choices, max_length=16, default=OrderStatus.IN_PROGRESS)


class ProviderOrder(models.Model):
    user = models.ForeignKey(PanelUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    status = models.CharField(choices=OrderStatus.choices, max_length=16, default=OrderStatus.IN_PROGRESS)
