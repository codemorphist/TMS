from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, UpdateView, DetailView
from django.views.generic.list import ListView

from panel.models import Product, ProductCategory, Provider, Client, Sale, Delivery
from panel.forms import ProductForm, ProductCategoryForm


def panel(request: HttpRequest) -> HttpResponse:
    """
    View for home page of panel
    """
    return render(request, 'panel/panel.html')


class ProductListView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'panel/product/product_list.html'
    context_object_name = 'products'


class ProductView(DetailView):
    model = Product
    template_name = 'panel/product/product_view.html'
    context_object_name = 'product'


def show_product(request: HttpRequest, product_id: str) -> HttpResponse:
    """
    Product page, show information about product
    """
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'panel/product/product_view.html', context=context)


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'category', 'description', 'price', 'count', 'providers']
    template_name = 'panel/product/product_edit.html'


class ProductFormView(FormView):
    template_name = 'panel/product/product_form.html'
    form_class = ProductForm

    def form_valid(self, form):
        self.product = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.product.get_absolute_url()


class ProductCategoryListView(ListView):
    model = ProductCategory
    paginate_by = 10
    template_name = 'panel/product_category/product_category_list.html'
    context_object_name = 'product_categories'


def show_product_category(request: HttpRequest, category: str) -> HttpResponse:
    category = get_object_or_404(ProductCategory, slug=category)
    products = category.products.all()
    context = {
        'category': category,
        'products': products,
    }
    return render(request,
                  'panel/product_category/product_category_view.html',
                  context=context)

def add_product_category(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            new_category = form
            return HttpResponseRedirect(new_category.get_absolute_url())

    form = ProductCategoryForm()
    context = {'form': form}
    return render(request,
                  'panel/product_category/product_category_add.html',
                  context=context)


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