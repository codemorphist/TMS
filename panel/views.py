from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404

from panel.models import Product, ProductCategory, Provider


def panel(request: HttpRequest) -> HttpResponse:
    """
    View for home page of panel
    """
    return render(request, 'panel/panel.html')


def show_products(request: HttpRequest) -> HttpResponse:
    """
    Products main page, that show table of all products
    """
    products = Product.objects.all().order_by('id')
    categories = ProductCategory.objects.all().order_by('id')
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'panel/products.html', context=context)


def show_product_category(request: HttpRequest, category: str) -> HttpResponse:
    category = get_object_or_404(ProductCategory, slug=category)
    products = category.products.all()
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'panel/product-category.html', context=context)


def show_product(request: HttpRequest, product_id: str) -> HttpResponse:
    """
    Product page, show information about product
    """
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'panel/product.html', context=context)


def show_providers(request: HttpRequest) -> HttpResponse:
    providers = Provider.objects.all()
    context = {
        'providers': providers,
    }
    return render(request, 'panel/providers.html', context=context)


def show_provider(request: HttpRequest, provider_id: int) -> HttpResponse:
    provider = get_object_or_404(Provider, id=provider_id)
    products = provider.products.all()
    context = {
        'provider': provider,
        'products': products,
    }
    return render(request, 'panel/provider.html', context=context)