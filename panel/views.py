from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from panel.models import Product, CatalogProduct
from users.models import Role
from users.utils import RoleBasedView, RoleRequiredMixin


class ClientPanelView(TemplateView):
    template_name = 'panel/panel.html'


class ProviderPanelView(TemplateView):
    template_name = 'panel/panel.html'


class OperatorPanelView(TemplateView):
    template_name = 'panel/panel.html'


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
    fields = ['name', 'category', 'description', 'price', 'count']
    template_name = 'panel/default/form.html'


class OperatorProductEditView(UpdateView):
    model = Product
    fields = ['name', 'category', 'description', 'price', 'count']
    template_name = 'panel/default/form.html'


class OperatorProductDeleteView(DeleteView):
    model = Product
    template_name = 'panel/default/delete_confirm.html'

    def get_success_url(self):
        return reverse('panel:products')


class AddProductView(RoleBasedView):
    views = {
        Role.PROVIDER: ProviderAddProductView.as_view(),
        # TODO: Role.OPERATOR
        # TODO: Role.CLIENT
    }


class CatalogProductsView(RoleRequiredMixin, ListView):
    model = CatalogProduct
    template_name = 'panel/catalog.html'
    context_object_name = 'products'
    paginate_by = 10
    allowed_roles = [Role.CLIENT, Role.OPERATOR]


