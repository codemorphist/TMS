from django.urls import path

from panel.views import *

app_name = 'panel'
urlpatterns = [
    path('', PanelView.as_view(), name='panel'),

    path('product/<int:pk>/', ProductView.as_view(),name='product'),
    path('products/', ProductsView.as_view(), name='products'),
    path('add-product/', AddProductView.as_view(), name='add-product'),
    path('products/edit/<int:pk>/', ProviderProductEditView.as_view(), name='edit-product'),
]



