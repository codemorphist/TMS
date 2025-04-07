from django.urls import path

import panel.views as views

urlpatterns = [
    path('', views.panel, name='panel'),
    path('products/', views.show_products, name='products'),
    path('product/<int:product_id>', views.show_product, name='product'),
    path('product-category/<slug:category>', views.show_product_category, name='product-category'),
    path('providers/', views.show_providers, name='providers'),
    path('provider/<int:provider_id>', views.show_provider, name='provider'),
]


