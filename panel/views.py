from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404

from panel.models import Product, ProductCategory, Provider, Client, Sale, Delivery


def panel(request: HttpRequest) -> HttpResponse:
    """
    View for home page of panel
    """
    return render(request, 'panel/panel.html')


def show_products(request: HttpRequest) -> HttpResponse:
    """
    Products main page, that show table of all products
    """
    categories = ProductCategory.objects.all().order_by('id')
    products = Product.objects.all().order_by('id').select_related('category')
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
    return render(request, 'panel/product_category.html', context=context)


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
    products = provider.products.all().select_related('category')
    context = {
        'provider': provider,
        'products': products,
    }
    return render(request, 'panel/provider.html', context=context)


def show_clients(request: HttpRequest) -> HttpResponse:
    clients = Client.objects.all()
    context = {
        'clients': clients,
    }
    return render(request, 'panel/clients.html', context=context)


def show_client(request: HttpRequest, client_id: int) -> HttpResponse:
    client = get_object_or_404(Client, id=client_id)
    context = {
        'client': client,
    }
    return render(request, 'panel/client.html', context=context)


def show_sales(request: HttpRequest) -> HttpResponse:
    sales = Sale.objects.all().select_related('product', 'client')
    context = {
        'sales': sales,
    }
    return render(request, 'panel/sales.html', context=context)


def show_sale(request: HttpRequest, sale_id: int) -> HttpResponse:
    sale = get_object_or_404(Sale, id=sale_id)
    context = {
        'sale': sale,
    }
    return render(request, 'panel/sale.html', context=context)


def show_deliveries(request: HttpRequest) -> HttpResponse:
    deliveries = Delivery.objects.all().select_related('product', 'provider')
    context = {
        'deliveries': deliveries,
    }
    return render(request, 'panel/deliveries.html', context=context)