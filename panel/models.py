from django.core.validators import MinValueValidator
from django.db import models

from users.models import PanelUser


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True)
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    provider = models.ForeignKey(PanelUser, on_delete=models.CASCADE, related_name='products')
