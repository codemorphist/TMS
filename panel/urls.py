from django.urls import path

import panel.views as views

app_name = 'panel'
urlpatterns = [
    path('', views.panel, name='panel'),

    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>', views.ProductView.as_view(), name='product'),
    path('add-product/', views.ProductFormView.as_view(), name='add-product'),
    path('edit-product/<int:pk>', views.ProductUpdateView.as_view(), name='edit-product'),

    path('product-categories/', views.ProductCategoryListView.as_view(), name='product-categories'),
    path('product-category/<slug:category>', views.show_product_category, name='product-category'),
    path('add-product-category/', views.add_product_category, name='add-product-category'),

    path('providers/', views.show_providers, name='providers'),
    path('provider/<int:provider_id>', views.show_provider, name='provider'),

    path('clients/', views.show_clients, name='clients'),
    path('client/<int:client_id>', views.show_client, name='client'),

    path('sales/', views.show_sales, name='sales'),
    path('sale/<int:sale_id>', views.show_sale, name='sale'),

    path('deliveries/', views.show_deliveries, name='deliveries'),
]



