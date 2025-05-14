from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, F
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from panel.forms import CatalogProductBuyForm
from users.models import PanelUser


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('panel:product', args=(self.pk,))

    def __str__(self):
        return f'{self.name}'


class CatalogProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('panel:catalog-product', args=(self.pk,))

    def buy_form(self):
        return CatalogProductBuyForm(product=self)

    def __str__(self):
        return f'{self.product.name}'


class OrderStatus(models.TextChoices):
    IN_PROGRESS = 'in_progress', 'In Progress'
    CANCELED = 'canceled', 'Canceled'
    COMPLETED = 'completed', 'Completed'


class ClientOrder(models.Model):
    user = models.ForeignKey(PanelUser, on_delete=models.CASCADE)
    product = models.ForeignKey(CatalogProduct, on_delete=models.CASCADE, related_name='orders')
    count = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    status = models.CharField(choices=OrderStatus.choices, max_length=16, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def total_price(self):
        return self.product.price * self.count

    def get_absolute_url(self):
        return reverse('panel:client-order', args=(self.pk,))

    def update_status(self, new_status: OrderStatus):
        order = self
        product = order.product
        status = order.status

        if status == new_status:
            return

        if new_status == OrderStatus.CANCELED:
            product.count = F('count') + order.count
        else:
            if product.count < order.count:
                raise ValidationError("Not enough product in stock.")
            product.count = F('count') - order.count
        order.status = new_status
        product.save()
        order.save()
        product.refresh_from_db()


class ProviderOrder(models.Model):
    user = models.ForeignKey(PanelUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    status = models.CharField(choices=OrderStatus.choices, max_length=16, default=OrderStatus.IN_PROGRESS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def total_price(self):
        return self.product.price * self.count
