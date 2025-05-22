from django.urls import path

from panel.views import *

app_name = 'panel'
urlpatterns = [
    path('', PanelView.as_view(), name='panel'),

    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('catalog/category/<int:pk>/', CategoryView.as_view(), name='category'),
    path('catalog/category/<int:pk>/edit', CategoryEditView.as_view(), name='edit-category'),
    path('catalog/category/<int:pk>/delete', CategoryDeleteView.as_view(), name='delete-category'),
    path('catalog/add-category/', CategoryAddView.as_view(), name='add-category'),

    path('catalog/product/<int:pk>/', ProductView.as_view(), name='product'),
    path('catalog/product/<int:pk>/edit', ProductEditView.as_view(), name='edit-product'),
    path('catalog/product/<int:pk>/delete', ProductDeleteView.as_view(), name='delete-product'),
    path('catalog/add-product/', ProductAddView.as_view(), name='add-product'),
    path('catalog/buy/', ProductBuyView.as_view(), name='buy-product'),

    path('orders/', OrdersView.as_view(), name='orders'),
    path('order/<int:pk>/', OrderView.as_view(), name='order'),
    path('order/<int:pk>/edit', OrderEditView.as_view(), name='edit-order'),
    path('order/<int:pk>/cancel', OrderCancelView.as_view(), name='cancel-order'),

    path('deliveries/', DeliveiesView.as_view(), name='deliveries'),
    path('devliveries/delivery/<int:pk>/', DeliveryView.as_view(), name='delivery'),
    path('deliveries/create-delivery/', DeliveryCreateView.as_view(), name='create-delivery'),
    path('devliveries/delivery/<int:pk>/edit', DeliveryEditView.as_view(), name='edit-delivery'),
    path('devliveries/delivery/<int:pk>/cancel', DeliveryCancelView.as_view(), name='cancel-delivery'),
    path('devliveries/delivery/<int:pk>/complete', DeliveryCompleteView.as_view(), name='complete-delivery'),
]



