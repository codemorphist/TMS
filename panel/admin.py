from django.contrib import admin

from panel.models import ProductCategory, Product, CatalogProduct
from users.models import PanelUser



class ProductAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "provider":
            kwargs["queryset"] = PanelUser.objects.filter(role='provider')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(CatalogProduct)