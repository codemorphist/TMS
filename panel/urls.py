from django.urls import path

from panel.views import *

app_name = 'panel'
urlpatterns = [
    path('', PanelView.as_view(), name='panel'),

    path('products/', ProductsView.as_view(), name='products'),
    path('products/add-product/', AddProductView.as_view(), name='add-product'),
    path('product/<int:pk>/', ProductView.as_view(), name='product'),
    path('product/edit/<int:pk>/', ProductEditView.as_view(), name='edit-product'),
    path('product/detele/<int:pk>', ProductDeleteView.as_view(), name='delete-product'),

    path('catalog/', CatalogProductsView.as_view(), name='catalog'),
    path('catalog/add-product/', AddCatalogProductView.as_view(), name='add-catalog-product'),
    path('catalog/product/<int:pk>', CatalogProductView.as_view(), name='catalog-product'),
    path('catalog/product/<int:pk>/edit/', CatalogProductEditView.as_view(), name='edit-catalog-product'),
    path('catalog/product/<int:pk>/delete/', CatalogProductDeleteView.as_view(), name='delete-catalog-product'),

    path('orders/', ClientOrdersViews.as_view(), name='client-orders'),
    path('order/<int:pk>/', ClientOrderView.as_view(), name='client-order'),
    path('order/<int:pk>/edit', ClientOrderEditView.as_view(), name='edit-client-order'),
    path('order/<int:pk>/cancel', ClientOrderCancelView.as_view(), name='cancel-client-order'),
    path('catalog/buy/<int:pk>/', ClientBuyOrderView.as_view(), name='client-buy'),

    path('sales/', OperatorSalesView.as_view(), name='sales'),

]



