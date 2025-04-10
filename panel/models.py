from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)
    category = models.ForeignKey('ProductCategory', on_delete=models.PROTECT, blank=True,
                                 related_name='products')
    providers = models.ManyToManyField('Provider', blank=True, related_name='products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('panel:product', kwargs={'product_id': self.id})


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('panel:product-category', kwargs={'category': self.slug})


class Provider(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('panel:provider', kwargs={'provider_id': self.id})


class Client(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('panel:client', kwargs={'client_id': self.id})


class Delivery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    count = models.IntegerField(default=0)
    price_for_one = models.FloatField(default=0.0)

    def __str__(self):
        return (f'{self.product.name} (x{self.count}) ({self.price_for_one})'
                f' <- {self.provider.name} [{self.provider.id}]')


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    count = models.IntegerField(default=0)
    price_for_one = models.FloatField(default=0.0)

    def __str__(self):
        return (f'{self.product.name} (x{self.count}) ({self.price_for_one})'
                f' -> {self.client.name} [{self.client.id}]')