from django.db import models
from django.urls import reverse


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

    def __str__(self):
        return f'{self.name}'
