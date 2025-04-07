from django.contrib import admin

from panel.models import Product, ProductCategory, Provider, Delivery

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Provider)
admin.site.register(Delivery)
