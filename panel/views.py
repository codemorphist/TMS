from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.list import ListView

from panel.models import Product, Category
from users.models import Role
from users.utils import RoleBasedView, RoleRequiredMixin


class PanelView(RoleRequiredMixin, TemplateView):
    allowed_roles = [Role.CLIENT, Role.PROVIDER, Role.OPERATOR]
    template_name = 'panel/panel.html'


class CatalogView(RoleRequiredMixin, ListView):
    allowed_roles = [Role.CLIENT, Role.OPERATOR]
    model = Product
    context_object_name = 'products'
    template_name = 'panel/catalog.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryView(RoleRequiredMixin, DetailView):
    allowed_roles = [Role.CLIENT, Role.OPERATOR]
    model = Category
    template_name = 'panel/category.html'
    context_object_name = 'category'


class CategoryAddView(RoleRequiredMixin, CreateView):
    allowed_roles = [Role.OPERATOR]
    model = Category
    fields = '__all__'
    template_name = 'panel/default/form.html'


class CategoryEditView(RoleRequiredMixin, UpdateView):
    allowed_roles = [Role.OPERATOR]
    model = Category
    fields = '__all__'
    template_name = 'panel/default/form.html'


class CategoryDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = [Role.OPERATOR]
    model = Category
    template_name = 'panel/default/delete_confirm.html'

    def get_success_url(self):
        return reverse('panel:catalog')


class ProductView(RoleRequiredMixin, DetailView):
    allowed_roles = [Role.CLIENT, Role.OPERATOR]
    model = Product
    context_object_name = 'product'
    template_name = 'panel/product.html'


class ProductAddView(RoleRequiredMixin, CreateView):
    allowed_roles = [Role.OPERATOR]
    model = Product
    fields = '__all__'
    template_name = 'panel/default/form.html'

    def get_success_url(self):
        return reverse('panel:catalog')


class ProductEditView(RoleRequiredMixin, UpdateView):
    allowed_roles = [Role.OPERATOR]
    model = Product
    fields = '__all__'
    template_name = 'panel/default/form.html'


class ProductDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = [Role.OPERATOR]
    model = Product
    template_name = 'panel/default/delete_confirm.html'

    def get_success_url(self):
        return reverse('panel:catalog')
