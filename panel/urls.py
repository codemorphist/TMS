from django.urls import path

import panel.views as views

urlpatterns = [
    path('', views.panel, name='panel'),
    path('products/', views.show_products, name='products'),
    path('product/<int:product_id>', views.show_product, name='product'),
]


