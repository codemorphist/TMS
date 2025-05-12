from django.urls import path

from panel.views import *

app_name = 'panel'
urlpatterns = [
    path('', PanelView.as_view(), name='panel'),

    path('products/', ProductsView.as_view(), name='products'),
    path('products/add-product/', AddProductView.as_view(), name='add-product'),
    path('product/<int:pk>/>', ProductView.as_view(), name='product'),
    path('product/edit/<int:pk>/', ProviderProductEditView.as_view(), name='edit-product'),
    path('product/detele/<int:pk>', ProviderProductDeleteView.as_view(), name='delete-product'),

    path('catalog/', CatalogProductsView.as_view(), name='catalog'),
]



