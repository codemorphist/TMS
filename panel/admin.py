from django.contrib import admin

from panel.models import Product, ProductCategory
from panel.models import Provider, Delivery
from panel.models import Client, Sale


admin.site.register(Product)
admin.site.register(ProductCategory)

admin.site.register(Provider)
admin.site.register(Delivery)

admin.site.register(Client)
admin.site.register(Sale)