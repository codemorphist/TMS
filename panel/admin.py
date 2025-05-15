from django.contrib import admin

from panel.models import Category, Product, Delivery, Order


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Delivery)
