from unittest import case

from django.contrib.auth import get_user_model
from django.db.models import F
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.list import ListView

from panel.forms import OrderForm
from panel.models import Product, Category, Order, OrderStatus, Delivery, DeliveryStatus

from users.models import Role
from users.utils import RoleRequiredMixin


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


class ProductBuyView(RoleRequiredMixin, View):
    allowed_roles = [Role.CLIENT]

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)

        if form.is_valid():
            product_pk = form.cleaned_data['product']
            product = Product.objects.get(pk=product_pk)
            quantity = form.cleaned_data['quantity']

            if quantity > product.stock:
                return HttpResponseBadRequest(form.errors)

            order = Order(client=request.user, product=product, quantity=quantity)
            product.stock = F('stock') - quantity
            order.save()
            product.save()

            return redirect(order.get_absolute_url())
        else:
            return HttpResponseBadRequest(form.errors)


class OrdersView(RoleRequiredMixin, ListView):
    allowed_roles = [Role.CLIENT, Role.OPERATOR]
    model = Order
    context_object_name = 'orders'
    template_name = 'panel/orders.html'

    def get_queryset(self):
        if self.request.user.role == Role.OPERATOR:
            return Order.objects.all()
        return Order.objects.filter(client=self.request.user)


class OrderView(RoleRequiredMixin, DetailView):
    allowed_roles = [Role.CLIENT, Role.OPERATOR]
    model = Order
    context_object_name = 'order'
    template_name = 'panel/order.html'

    def get_queryset(self):
        if self.request.user.role == Role.OPERATOR:
            return Order.objects.all()
        return Order.objects.filter(client=self.request.user)


class OrderEditView(RoleRequiredMixin, UpdateView):
    allowed_roles = [Role.OPERATOR]
    model = Order
    fields = ['status']
    template_name = 'panel/default/form.html'

    def form_valid(self, form):
        order = self.get_object()
        new_status = form.cleaned_data['status']
        order.update_status(new_status)
        return super().form_valid(form)


class OrderCancelView(RoleRequiredMixin, View):
    allowed_roles = [Role.CLIENT, Role.OPERATOR]

    def get(self, request, pk: int):
        order = get_object_or_404(Order, pk=pk)

        if request.user.role == Role.CLIENT:
            if order.client != request.user:
                raise Http404('Order not found')

        match order.status:
            case OrderStatus.CANCELED:
                return HttpResponseBadRequest('Order already canceled.')
            case OrderStatus.COMPLETED:
                return HttpResponseBadRequest('Can\'n cancel completed order')

        order.update_status(OrderStatus.CANCELED)
        return redirect(order.get_absolute_url())


class DeliveiesView(RoleRequiredMixin, ListView):
    allowed_roles = [Role.PROVIDER, Role.OPERATOR]
    model = Delivery
    template_name = 'panel/deliveries.html'
    context_object_name = 'deliveries'

    def get_queryset(self):
        if self.request.user.role == Role.OPERATOR:
            return Delivery.objects.all()
        return Delivery.objects.filter(provider=self.request.user)


class DeliveryView(RoleRequiredMixin, DetailView):
    allowed_roles = [Role.PROVIDER, Role.OPERATOR]
    model = Delivery
    context_object_name = 'delivery'
    template_name = 'panel/delivery.html'

    def get_queryset(self):
        if self.request.user.role == Role.OPERATOR:
            return Delivery.objects.all()
        return Delivery.objects.filter(provider=self.request.user)


class DeliveryCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = [Role.OPERATOR]
    model = Delivery
    fields = ['provider', 'product', 'quantity']
    template_name = 'panel/default/form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        User = get_user_model()
        form.fields['provider'].queryset = User.objects.filter(role=Role.PROVIDER)
        return form

    def get_success_url(self):
        return reverse('panel:deliveries')


class DeliveryCancelView(RoleRequiredMixin, View):
    allowed_roles = [Role.PROVIDER, Role.OPERATOR]

    def get(self, request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)

        if request.user.role == Role.PROVIDER:
            if delivery.provider != request.user:
                raise Http404('Delivery not found')

        match delivery.status:
            case OrderStatus.CANCELED:
                return HttpResponseBadRequest('Delivery already canceled.')
            case OrderStatus.COMPLETED:
                return HttpResponseBadRequest('Can\'t cancel completed delivery.')

        delivery.update_status(DeliveryStatus.CANCELED)

        return redirect(delivery.get_absolute_url())


class DeliveryCompleteView(RoleRequiredMixin, View):
    allowed_roles = [Role.OPERATOR]

    def get(self, request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)

        match delivery.status:
            case OrderStatus.COMPLETED:
                return HttpResponseBadRequest('Delivery already completed.')
            case OrderStatus.CANCELED:
                return HttpResponseBadRequest('Delivery already canceled.')

        delivery.update_status(DeliveryStatus.COMPLETED)
        return redirect(delivery.get_absolute_url())


class DeliveryEditView(RoleRequiredMixin, UpdateView):
    allowed_roles = [Role.OPERATOR]
    model = Delivery
    fields = ['status']
    template_name = 'panel/default/form.html'

    def form_valid(self, form):
        delivery = self.get_object()
        new_status = form.cleaned_data['status']
        delivery.update_status(new_status)
        return super().form_valid(form)