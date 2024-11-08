from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _


from order.models import UserCart, CartItem
from store.models import Product


class CartView(LoginRequiredMixin, TemplateView):
    login_url = '/user/login/'
    template_name = 'cart.html'
    title = _('Cart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class CheckoutView(LoginRequiredMixin, TemplateView):
    login_url = '/user/login/'
    template_name = 'checkout.html'
    title = _('Checkout')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class AddToCartForm(forms.Form):
    product_id = forms.ModelChoiceField(queryset=Product.objects.all())


class AddToCartView(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def _err_out_of_stock(self, request, product):
        messages.error(
            request, _("Only %s items available in stock.") % product.name)

    def post(self, request, *args, **kwargs):
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product_id']

            in_stock = product.quantity >= 1
            if not in_stock:
                self._err_out_of_stock(request, product)
                return redirect(request.META.get('HTTP_REFERER', '/'))

            cart, created = UserCart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product)

            if not created:
                in_stock = product.quantity >= cart_item.quantity + 1
                if not in_stock:
                    self._err_out_of_stock(request, product)
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                cart_item.quantity += 1

            cart_item.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class RemoveFromCartForm(forms.Form):
    product_id = forms.ModelChoiceField(queryset=Product.objects.all())
    remove_all = forms.BooleanField(required=False)


class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def post(self, request, *args, **kwargs):
        form = RemoveFromCartForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product_id']
            remove_all = form.cleaned_data['remove_all']

            try:
                cart = UserCart.objects.get(user=request.user)
                cart_item = CartItem.objects.get(cart=cart, product=product)

                if remove_all:
                    cart_item.delete()
                    messages.success(
                        request, _("%s removed from cart.") % product.name)
                else:
                    if cart_item.quantity > 1:
                        cart_item.quantity -= 1
                        cart_item.save()
                        messages.success(
                            request, _("Removed one %s from cart.") % product.name)
                    else:
                        cart_item.delete()
                        messages.success(
                            request, _("Last %s removed from cart.") % product.name)

            except (UserCart.DoesNotExist, CartItem.DoesNotExist):
                messages.error(request, _("Item not found in cart."))

            finally:
                return redirect(request.META.get('HTTP_REFERER', '/'))

        messages.error(request, _("Invalid request."))
