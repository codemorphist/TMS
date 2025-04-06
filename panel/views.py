from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404

from panel.models import Product


def panel(request: HttpRequest) -> HttpResponse:
    """
    View for home page of panel
    """
    return render(request, 'panel/panel.html')


def show_products(request: HttpRequest) -> HttpResponse:
    """
    Products main page, that show table of all products
    """
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'panel/products.html', context=context)


def show_product(request: HttpRequest, product_id: int) -> HttpResponse:
    """
    Product page, show information about product
    """
    product = Product.objects.get(id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'panel/product.html', context=context)