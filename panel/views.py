from django.contrib.auth import get_user_model
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.test import Client
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from panel.forms import ClientBuyForm
from panel.models import Product, CatalogProduct, ClientOrder, OrderStatus
from users.models import Role
from users.utils import RoleBasedView, RoleRequiredMixin


class ClientPanelView(TemplateView):
    template_name = 'panel/panel.html'


class ProviderPanelView(TemplateView):
    template_name = 'panel/panel.html'


class OperatorPanelView(TemplateView):
    template_name = 'panel/panel.html'


# TODO: Refactor and delete to TemplateView
class PanelView(RoleBasedView):
    views = {
        Role.CLIENT: ClientPanelView.as_view(),
        Role.PROVIDER: ProviderPanelView.as_view(),
        Role.OPERATOR: OperatorPanelView.as_view(),
    }


class ProviderProductView(DetailView):
    model = Product
    template_name = 'panel/product.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.provider != self.request.user:
            raise Http404()
        return obj


class OperatorProductView(DetailView):
    model = Product
    template_name = 'panel/product.html'
    context_object_name =  'product'


class ProductView(RoleBasedView):
    views = {
        Role.PROVIDER: ProviderProductView.as_view(),
        Role.OPERATOR: OperatorProductView.as_view(),
    }


class ProviderProductsView(ListView):
    model = Product
    template_name = 'panel/products.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.products.all()


class OperatorProductsView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'panel/products.html'
    context_object_name = 'products'


class ProductsView(RoleBasedView):
    views = {
        Role.PROVIDER: ProviderProductsView.as_view(),
        Role.OPERATOR: OperatorProductsView.as_view(),
    }


class ProviderAddProductView(CreateView):
    model = Product
    fields = ['name', 'category', 'description', 'price', 'count']
    template_name = 'panel/default/form.html'

    def form_valid(self, form):
        form.instance.provider = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('panel:products')


class ProviderProductEditView(UpdateView):
    model = Product
    fields = ['name', 'category', 'description', 'price', 'count']
    template_name = 'panel/default/form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.provider != self.request.user:
            raise Http404()
        return obj


class ProviderProductDeleteView(DeleteView):
    model = Product
    template_name = 'panel/default/delete_confirm.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.provider != self.request.user:
            raise Http404()
        return obj

    def get_success_url(self):
        return reverse('panel:products')


class OperatorAddProductView(CreateView):
    model = Product
    fields = ['name', 'category', 'description', 'price', 'count', 'provider']
    template_name = 'panel/default/form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        UserModel = get_user_model()
        form.fields['provider'].queryset = UserModel.objects.filter(role=Role.PROVIDER)
        return form


class OperatorProductEditView(UpdateView):
    model = Product
    fields = ['name', 'category', 'description', 'price', 'count', 'provider']
    template_name = 'panel/default/form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        UserModel = get_user_model()
        form.fields['provider'].queryset = UserModel.objects.filter(role=Role.PROVIDER)
        return form


class OperatorProductDeleteView(DeleteView):
    model = Product
    template_name = 'panel/default/delete_confirm.html'

    def get_success_url(self):
        return reverse('panel:products')


class AddProductView(RoleBasedView):
    views = {
        Role.PROVIDER: ProviderAddProductView.as_view(),
        Role.OPERATOR: OperatorAddProductView.as_view(),
    }


class ProductEditView(RoleBasedView):
    views = {
        Role.PROVIDER: ProviderProductEditView.as_view(),
        Role.OPERATOR: OperatorProductEditView.as_view(),
    }


class ProductDeleteView(RoleBasedView):
    views = {
        Role.PROVIDER: ProviderProductDeleteView.as_view(),
        Role.OPERATOR: OperatorProductDeleteView.as_view(),
    }


class CatalogProductsView(RoleRequiredMixin, ListView):
    model = CatalogProduct
    template_name = 'panel/catalog.html'
    context_object_name = 'products'
    paginate_by = 10
    allowed_roles = [Role.CLIENT, Role.OPERATOR]

    def get_queryset(self):
        products = CatalogProduct.objects.all()
        if self.request.user.role != Role.CLIENT:
            return products

        for product in products:
            product.buy_form = ClientBuyForm(
                initial={'product_id': product.pk},
                max_count=product.count
            )

        return products


class CatalogProductView(RoleRequiredMixin, DetailView):
    model = CatalogProduct
    template_name = 'panel/catalog_product.html'
    context_object_name = 'product'
    allowed_roles = [Role.CLIENT, Role.OPERATOR]


class AddCatalogProductView(RoleRequiredMixin, CreateView):
    model = CatalogProduct
    fields = ['product', 'price', 'count']
    template_name = 'panel/default/form.html'
    allowed_roles = [Role.OPERATOR]

    def form_valid(self, form):
        product = form.cleaned_data['product']
        if CatalogProduct.objects.filter(product=product).exists():
            form.add_error('product', 'This product is already in the catalog.')
            return self.form_invalid(form)
        return super().form_valid(form)


class CatalogProductEditView(RoleRequiredMixin, UpdateView):
    model = CatalogProduct
    fields = ['price', 'count']
    template_name = 'panel/default/form.html'
    allowed_roles = [Role.OPERATOR]


class CatalogProductDeleteView(RoleRequiredMixin, DeleteView):
    model = CatalogProduct
    template_name = 'panel/default/delete_confirm.html'
    allowed_roles = [Role.CLIENT, Role.OPERATOR]

    def get_success_url(self):
        return reverse('panel:catalog')


class ClientOrdersViews(RoleRequiredMixin, ListView):
    model = ClientOrder
    template_name = 'panel/client_orders.html'
    context_object_name = 'orders'
    paginate_by = 10
    allowed_roles = [Role.CLIENT]

    def get_queryset(self):
        user = self.request.user
        return ClientOrder.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = context['orders']

        for order in orders:
            order.total_price = order.product.price * order.count

        return context


class ClientBuyOrderView(RoleRequiredMixin, View):
    allowed_roles = [Role.CLIENT]

    def post(self, request, *args, **kwargs):
        form = ClientBuyForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            count = form.cleaned_data['count']
            product = get_object_or_404(CatalogProduct, pk=product_id)
            if count > product.count:
                form.add_error('count', 'Invalid product count.')
            else:
                order = ClientOrder(
                    user=request.user,
                    product=product,
                    count=count,
                    status=OrderStatus.IN_PROGRESS,
                )
                order.save()
                product.count = F('count') - count
                product.save()
        return redirect('panel:client-orders')


class OperatorSalesView(RoleRequiredMixin, ListView):
    model = ClientOrder
    template_name = 'panel/operator_sales.html'
    context_object_name = 'sales'
    allowed_roles = [Role.OPERATOR]

    def get_queryset(self):
        sales = ClientOrder.objects.all()

        for sale in sales:
            sale.total_price = sale.product.price * sale.count

        return sales
